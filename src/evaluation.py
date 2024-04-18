import argparse
import asyncio
import json
import os
import time
import uuid
import nest_asyncio
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
    BatchEvalRunner,
    DatasetGenerator,
    RelevancyEvaluator,
    QueryResponseDataset
)
from llama_index.core import Settings,  ServiceContext, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llms.llm_loader import LLMLoader

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore

# Constant

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def eval_parser(eval_response: str) :
    """
    Default parser function for evaluation response.

    Args:
        eval_response (str): The response string from the evaluation.

    Returns:
        Tuple[float, str]: A tuple containing the score as a float and the reasoning as a string.
    """
    
    print("eval_response:", eval_response)
    
    eval_response_parsed = eval_response.split("\n")
    eval_len =len (eval_response_parsed)
    
    if eval_len == 0 :
        return 0, eval_response_parsed
    if eval_len == 1 :
        return 0, eval_response_parsed 
    if eval_len == 2 : 
        score_str =  eval_response_parsed[0]
        score = float(score_str) if is_float(score_str) else 0 
        reasoning = eval_response_parsed[1]
        return score, reasoning
        
    if eval_len == 3 : 
        score_str, reasoning_str =  eval_response_parsed[1], eval_response_parsed[2]    
        score = float(score_str) if is_float(score_str) else 0 
        reasoning = reasoning_str.lstrip("\n")
        return score, reasoning
    if eval_len > 3 : 
        return 0, eval_response

def load_question_from_folder(folder):
    with open(folder, 'r') as file:
        question_object  = json.load(file)
        queries = {}
        for dir in question_object["evaluation-results"]: 

            for q in dir.get("questions"): 
                cur_queries = {
                    str(uuid.uuid4()): q
                }
                queries.update(cur_queries)
        return  QueryResponseDataset(queries=queries)  

def get_eval_results(key, eval_results):
    results = eval_results[key]
    correct = 0
    for result in results:
        if result.passing:
            correct += 1
    score = correct / len(results)
    print(f"{key} Score: {score}")
    return score

async def main(): 
    start_time = time.time()
    # collect args 
    parser = argparse.ArgumentParser(
        description="evaluation cli for task execution"
    )
    parser.add_argument("-p", "--provider",   default="bam", help="LLM provider supported value: bam, openai")
    parser.add_argument("-m", "--model",   default="local:BAAI/bge-base-en", help="the valid models are:\
                                                                    - ibm/granite-13b-chat-v1, ibm/granite-13b-chat-v2, ibm/granite-20b-code-instruct-v1 for bam \
                                                                    - gpt-3.5-turbo-1106, gpt-3.5-turbo for openai"
                        )    
    parser.add_argument("-x", "--product-index" ,default="product" , help="storage product index")
    parser.add_argument("-i", "--input-persist-dir" , help="path to persist file dir")
    parser.add_argument("-gq", "--generate-questions", type=bool,   default="", help="should generate question")    
    parser.add_argument("-q", "--question-doc-folder",   default="", help="docs folder for questions gen")
    parser.add_argument("-lq", "--load-question-file",   default="", help="load question from folder")
    parser.add_argument("-n", "--number-of-questions" ,type=int, default="5" , help="number of questions used for evaluation")
    parser.add_argument("-s", "--similarity" , type=int,  default="5" , help="similarity_top_k")
    parser.add_argument("-c", "--chunk", type=int ,  default="500", help="chunk size for embedding")
    parser.add_argument("-l", "--overlap", type=int,  default="50", help="chunk overlap for embedding")
    parser.add_argument("-o", "--output", help="persist folder")
    parser.add_argument(
                    "-md",
                    "--model-dir",
                    default="embeddings_model",
                    help="Directory containing the embedding model",
                    )

    # execute 
    args = parser.parse_args() 
    
    print(" --> settings context")
    PERSIST_FOLDER = args.output
    PRODUCT_INDEX=args.product_index
    PRODUCT_DOCS_PERSIST_DIR = args.input_persist_dir
    NUM_OF_QUESTIONS=args.number_of_questions
    SIMILARITY=args.similarity

    os.environ["HF_HOME"] = args.model_dir
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    Settings.chunk_size = args.chunk
    Settings.chunk_overlap = args.overlap
    Settings.embed_model = HuggingFaceEmbedding(model_name=args.model_dir)
        
    print(" --> settings params")
        
    embed_model = "local:BAAI/bge-base-en"        
    Settings.llm = LLMLoader(args.provider, args.model).llm  
    bare_llm = LLMLoader(args.provider, args.model).llm
    service_context = ServiceContext.from_defaults(llm=bare_llm, embed_model=embed_model)         
    
    print(" --> load embeddings evaluating")

    # load index from disk
    vector_store = FaissVectorStore.from_persist_dir(PRODUCT_DOCS_PERSIST_DIR)
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store, persist_dir=PRODUCT_DOCS_PERSIST_DIR
    )
    index = load_index_from_storage(storage_context=storage_context,index_id=PRODUCT_INDEX)


    print(" --> starting model evaluating")
    nest_asyncio.apply()
    
    print(" --> generating questions") 
    if args.generate_questions:       
        question_folder = args.folder if args.question_doc_folder is None else args.question_doc_folder
        reader = SimpleDirectoryReader(question_folder)
        question = reader.load_data()
        data_generator = DatasetGenerator.from_documents(question)
        eval_questions = data_generator.generate_dataset_from_nodes(num=NUM_OF_QUESTIONS)
        
    if args.load_question_file: 
        eval_questions = load_question_from_folder(args.load_question_file) 
    
    
    print(" --> start evaluation")
    faithfulness = FaithfulnessEvaluator(service_context=service_context)
    relevancy = RelevancyEvaluator(service_context=service_context)
    correctness = CorrectnessEvaluator(service_context=service_context,score_threshold=2.0 ,parser_function=eval_parser)

    runner = BatchEvalRunner(
                                { "faithfulness": faithfulness, "relevancy": relevancy},
                                    workers=8, show_progress=True
                            )

    eval_results = await runner.aevaluate_queries(  index.as_chat_engine(), eval_questions.questions[:5] )
    
    evaluation_results = {}
    evaluation_results["faithfulness"] = get_eval_results("faithfulness", eval_results)
    evaluation_results["relevancy"] = get_eval_results("relevancy", eval_results)
    
    # correctness test
    engine = index.as_chat_engine(similarity_top_k=SIMILARITY, service_context=service_context)
        

    
    total_correctness_score = []
    res_table = []
    for query in eval_questions.questions: 
        res_row ={}                
        summary = engine.query(query)
        referenced_documents = "\n".join(
            [
                source_node.node.metadata["file_name"]
                for source_node in summary.source_nodes
            ]
        )
        
        result =correctness.evaluate(
            query=query,
            response=summary.response,
            reference=summary.source_nodes[0].text if len(summary.source_nodes)>0 else None 
            )
        
        res_row["question"] = query
        res_row["response"] = summary.response
        res_row["ref"] = referenced_documents 
        res_row["ref_doc"] = summary.source_nodes[0].text if len(summary.source_nodes)>0 else None 
        res_row["ref_doc_score"] = summary.source_nodes[0].score if len(summary.source_nodes)>0 else None 
        res_row["passing"] = result.passing
        res_row["feedback"] = result.feedback
        res_row["score"] = result.score
        total_correctness_score.append(float(result.score))
        
        res_table.append(res_row)

    evaluation_results["correctness"] = res_table

    end_time = time.time()
    execution_time_seconds = end_time - start_time 
    print(f"** Total execution time in seconds: {execution_time_seconds}")
    
    # creating metadata folder 
    metadata = {} 
    metadata["execution-time"] = execution_time_seconds
    metadata["llm"] = args.provider
    metadata["model"] = args.model 
    metadata["index_id"] = PRODUCT_INDEX
    metadata["eval_questions"] = eval_questions.questions
    metadata["correctness-results"] = sum(total_correctness_score) / len(total_correctness_score)
    metadata["evaluation_results"] = evaluation_results
    json_metadata = json.dumps(metadata)
    
    if not os.path.exists(PERSIST_FOLDER):
        os.makedirs(PERSIST_FOLDER) 
    model_name_formatted = args.model.replace("/","_")

    # Write the JSON data to a file
    file_path = f"{PERSIST_FOLDER}/{args.provider}-{model_name_formatted}_metadata.md"
    with open(file_path, 'w') as file:
        file.write(json_metadata)
    
    # Convert JSON data to markdown 
    markdown_content = "```markdown\n"
    for key, value in metadata.items():
        markdown_content += f"- {key}: {value}\n"
    markdown_content += "```" 
    
    file_path = f"{PERSIST_FOLDER}/{args.provider}-{model_name_formatted}_metadata.md"
    with open(file_path, 'w') as file:
        file.write(markdown_content)
    return "Completed"
    
asyncio.run(main())