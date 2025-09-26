# asciidoc structure dumper script
#

require 'asciidoctor'

# Function to recursively dump object structures
def dump_structure(node, indent = 0)
  indent_str = ' ' * indent
  node_info = "#{indent_str}#<#{node.class.name}"

  # Collecting attributes
  attributes = {}
  if node.respond_to?(:context)
    attributes[:context] = node.context
  end
  if node.respond_to?(:title)
    attributes[:title] = node.title
  end
  if node.respond_to?(:level)
    attributes[:level] = node.level
  end
  if node.respond_to?(:text)
    attributes[:text] = node.text
  end
  if node.respond_to?(:blocks)
    attributes[:blocks] = node.blocks.size
  end

  # Adding attributes to the node info
  unless attributes.empty?
    attributes_str = attributes.map { |key, value| "#{key}: #{value.inspect}" }.join(', ')
    node_info += " {#{attributes_str}}"
  end
  node_info += '>'

  puts node_info

  # Recursively process child blocks
  if node.respond_to?(:blocks) && node.blocks.any?
    node.blocks.each { |child| dump_structure(child, indent + 2) }
  end
end

# Load and parse the AsciiDoc file
def load_and_dump_asciidoc(file_path)
  # Read the file content
  asciidoc_content = File.read(file_path)

  # Parse the AsciiDoc content
  doc = Asciidoctor.load(asciidoc_content)

  # Dump the structure of the document
  dump_structure(doc)
end

# Check if the script is run with a file path argument
if ARGV.size != 1
  puts "Usage: ruby asciidoc_structure_dumper.rb <path_to_asciidoc_file>"
  exit 1
end

# Load and process the AsciiDoc file
file_path = ARGV[0]
load_and_dump_asciidoc(file_path)
