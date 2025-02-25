---
language:
- en
license: apache-2.0
library_name: transformers
tags:
- language
- granite
- embeddings
- mteb
model-index:
- name: ibm-granite/granite-embedding-125m-english
  results:
  - dataset:
      config: en-ext
      name: MTEB AmazonCounterfactualClassification (en-ext)
      revision: e8379541af4e31359cca9fbcf4b00f2671dba205
      split: test
      type: mteb/amazon_counterfactual
    metrics:
    - type: accuracy
      value: 67.3613
    - type: f1
      value: 55.0794
    - type: f1_weighted
      value: 73.55120000000001
    - type: ap
      value: 17.643900000000002
    - type: ap_weighted
      value: 17.643900000000002
    - type: main_score
      value: 67.3613
    task:
      type: Classification
  - dataset:
      config: en
      name: MTEB AmazonCounterfactualClassification (en)
      revision: e8379541af4e31359cca9fbcf4b00f2671dba205
      split: test
      type: mteb/amazon_counterfactual
    metrics:
    - type: accuracy
      value: 63.403
    - type: f1
      value: 57.4178
    - type: f1_weighted
      value: 66.9704
    - type: ap
      value: 26.892300000000002
    - type: ap_weighted
      value: 26.892300000000002
    - type: main_score
      value: 63.403
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB AmazonPolarityClassification (default)
      revision: e2d317d38cd51312af73b3d32a06d1a08b442046
      split: test
      type: mteb/amazon_polarity
    metrics:
    - type: accuracy
      value: 64.5872
    - type: f1
      value: 64.33330000000001
    - type: f1_weighted
      value: 64.33330000000001
    - type: ap
      value: 59.602
    - type: ap_weighted
      value: 59.602
    - type: main_score
      value: 64.5872
    task:
      type: Classification
  - dataset:
      config: en
      name: MTEB AmazonReviewsClassification (en)
      revision: 1399c76144fd37290681b995c656ef9b2e06e26d
      split: test
      type: mteb/amazon_reviews_multi
    metrics:
    - type: accuracy
      value: 33.534000000000006
    - type: f1
      value: 32.5389
    - type: f1_weighted
      value: 32.5389
    - type: main_score
      value: 33.534000000000006
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB AppsRetrieval (default)
      revision: f22508f96b7a36c2415181ed8bb76f76e04ae2d5
      split: test
      type: CoIR-Retrieval/apps
    metrics:
    - type: ndcg_at_1
      value: 6.932
    - type: ndcg_at_3
      value: 9.577
    - type: ndcg_at_5
      value: 10.597
    - type: ndcg_at_10
      value: 11.787
    - type: ndcg_at_20
      value: 12.863
    - type: ndcg_at_100
      value: 15.573999999999998
    - type: ndcg_at_1000
      value: 19.772000000000002
    - type: map_at_1
      value: 6.932
    - type: map_at_3
      value: 8.938
    - type: map_at_5
      value: 9.506
    - type: map_at_10
      value: 10.0
    - type: map_at_20
      value: 10.296
    - type: map_at_100
      value: 10.644
    - type: map_at_1000
      value: 10.771
    - type: recall_at_1
      value: 6.932
    - type: recall_at_3
      value: 11.421000000000001
    - type: recall_at_5
      value: 13.891
    - type: recall_at_10
      value: 17.556
    - type: recall_at_20
      value: 21.806
    - type: recall_at_100
      value: 36.839
    - type: recall_at_1000
      value: 71.71300000000001
    - type: precision_at_1
      value: 6.932
    - type: precision_at_3
      value: 3.807
    - type: precision_at_5
      value: 2.778
    - type: precision_at_10
      value: 1.756
    - type: precision_at_20
      value: 1.09
    - type: precision_at_100
      value: 0.368
    - type: precision_at_1000
      value: 0.07200000000000001
    - type: mrr_at_1
      value: 6.9323
    - type: mrr_at_3
      value: 8.9376
    - type: mrr_at_5
      value: 9.506
    - type: mrr_at_10
      value: 9.9999
    - type: mrr_at_20
      value: 10.2957
    - type: mrr_at_100
      value: 10.643600000000001
    - type: mrr_at_1000
      value: 10.7707
    - type: nauc_ndcg_at_1_max
      value: 27.327299999999997
    - type: nauc_ndcg_at_1_std
      value: 9.6266
    - type: nauc_ndcg_at_1_diff1
      value: 39.4451
    - type: nauc_ndcg_at_3_max
      value: 22.9053
    - type: nauc_ndcg_at_3_std
      value: 10.123
    - type: nauc_ndcg_at_3_diff1
      value: 27.742099999999997
    - type: nauc_ndcg_at_5_max
      value: 21.7041
    - type: nauc_ndcg_at_5_std
      value: 9.661100000000001
    - type: nauc_ndcg_at_5_diff1
      value: 25.0689
    - type: nauc_ndcg_at_10_max
      value: 21.0966
    - type: nauc_ndcg_at_10_std
      value: 10.4106
    - type: nauc_ndcg_at_10_diff1
      value: 23.4219
    - type: nauc_ndcg_at_20_max
      value: 20.0575
    - type: nauc_ndcg_at_20_std
      value: 10.89
    - type: nauc_ndcg_at_20_diff1
      value: 22.6143
    - type: nauc_ndcg_at_100_max
      value: 19.4243
    - type: nauc_ndcg_at_100_std
      value: 11.5431
    - type: nauc_ndcg_at_100_diff1
      value: 21.013
    - type: nauc_ndcg_at_1000_max
      value: 20.6057
    - type: nauc_ndcg_at_1000_std
      value: 13.0027
    - type: nauc_ndcg_at_1000_diff1
      value: 20.988799999999998
    - type: nauc_map_at_1_max
      value: 27.327299999999997
    - type: nauc_map_at_1_std
      value: 9.6266
    - type: nauc_map_at_1_diff1
      value: 39.4451
    - type: nauc_map_at_3_max
      value: 23.6991
    - type: nauc_map_at_3_std
      value: 9.9287
    - type: nauc_map_at_3_diff1
      value: 29.909799999999997
    - type: nauc_map_at_5_max
      value: 22.9242
    - type: nauc_map_at_5_std
      value: 9.640600000000001
    - type: nauc_map_at_5_diff1
      value: 28.228199999999998
    - type: nauc_map_at_10_max
      value: 22.612199999999998
    - type: nauc_map_at_10_std
      value: 10.0051
    - type: nauc_map_at_10_diff1
      value: 27.3942
    - type: nauc_map_at_20_max
      value: 22.236
    - type: nauc_map_at_20_std
      value: 10.168000000000001
    - type: nauc_map_at_20_diff1
      value: 27.0258
    - type: nauc_map_at_100_max
      value: 22.1373
    - type: nauc_map_at_100_std
      value: 10.2741
    - type: nauc_map_at_100_diff1
      value: 26.717800000000004
    - type: nauc_map_at_1000_max
      value: 22.1829
    - type: nauc_map_at_1000_std
      value: 10.3395
    - type: nauc_map_at_1000_diff1
      value: 26.7158
    - type: nauc_recall_at_1_max
      value: 27.327299999999997
    - type: nauc_recall_at_1_std
      value: 9.6266
    - type: nauc_recall_at_1_diff1
      value: 39.4451
    - type: nauc_recall_at_3_max
      value: 21.0841
    - type: nauc_recall_at_3_std
      value: 10.6057
    - type: nauc_recall_at_3_diff1
      value: 22.745
    - type: nauc_recall_at_5_max
      value: 19.0389
    - type: nauc_recall_at_5_std
      value: 9.697899999999999
    - type: nauc_recall_at_5_diff1
      value: 18.137600000000003
    - type: nauc_recall_at_10_max
      value: 18.0668
    - type: nauc_recall_at_10_std
      value: 11.326799999999999
    - type: nauc_recall_at_10_diff1
      value: 15.423
    - type: nauc_recall_at_20_max
      value: 15.798100000000002
    - type: nauc_recall_at_20_std
      value: 12.4585
    - type: nauc_recall_at_20_diff1
      value: 14.509500000000001
    - type: nauc_recall_at_100_max
      value: 14.2836
    - type: nauc_recall_at_100_std
      value: 14.2989
    - type: nauc_recall_at_100_diff1
      value: 10.7304
    - type: nauc_recall_at_1000_max
      value: 19.728299999999997
    - type: nauc_recall_at_1000_std
      value: 24.5691
    - type: nauc_recall_at_1000_diff1
      value: 6.1472999999999995
    - type: nauc_precision_at_1_max
      value: 27.327299999999997
    - type: nauc_precision_at_1_std
      value: 9.6266
    - type: nauc_precision_at_1_diff1
      value: 39.4451
    - type: nauc_precision_at_3_max
      value: 21.0841
    - type: nauc_precision_at_3_std
      value: 10.6057
    - type: nauc_precision_at_3_diff1
      value: 22.745
    - type: nauc_precision_at_5_max
      value: 19.0389
    - type: nauc_precision_at_5_std
      value: 9.697899999999999
    - type: nauc_precision_at_5_diff1
      value: 18.137600000000003
    - type: nauc_precision_at_10_max
      value: 18.0668
    - type: nauc_precision_at_10_std
      value: 11.326799999999999
    - type: nauc_precision_at_10_diff1
      value: 15.423
    - type: nauc_precision_at_20_max
      value: 15.798100000000002
    - type: nauc_precision_at_20_std
      value: 12.4585
    - type: nauc_precision_at_20_diff1
      value: 14.509500000000001
    - type: nauc_precision_at_100_max
      value: 14.2836
    - type: nauc_precision_at_100_std
      value: 14.2989
    - type: nauc_precision_at_100_diff1
      value: 10.7304
    - type: nauc_precision_at_1000_max
      value: 19.728299999999997
    - type: nauc_precision_at_1000_std
      value: 24.5691
    - type: nauc_precision_at_1000_diff1
      value: 6.1472999999999995
    - type: nauc_mrr_at_1_max
      value: 27.327299999999997
    - type: nauc_mrr_at_1_std
      value: 9.6266
    - type: nauc_mrr_at_1_diff1
      value: 39.4451
    - type: nauc_mrr_at_3_max
      value: 23.6991
    - type: nauc_mrr_at_3_std
      value: 9.9287
    - type: nauc_mrr_at_3_diff1
      value: 29.909799999999997
    - type: nauc_mrr_at_5_max
      value: 22.9242
    - type: nauc_mrr_at_5_std
      value: 9.640600000000001
    - type: nauc_mrr_at_5_diff1
      value: 28.228199999999998
    - type: nauc_mrr_at_10_max
      value: 22.612199999999998
    - type: nauc_mrr_at_10_std
      value: 10.0051
    - type: nauc_mrr_at_10_diff1
      value: 27.3942
    - type: nauc_mrr_at_20_max
      value: 22.236
    - type: nauc_mrr_at_20_std
      value: 10.168000000000001
    - type: nauc_mrr_at_20_diff1
      value: 27.0258
    - type: nauc_mrr_at_100_max
      value: 22.1372
    - type: nauc_mrr_at_100_std
      value: 10.2743
    - type: nauc_mrr_at_100_diff1
      value: 26.7177
    - type: nauc_mrr_at_1000_max
      value: 22.1828
    - type: nauc_mrr_at_1000_std
      value: 10.3397
    - type: nauc_mrr_at_1000_diff1
      value: 26.7157
    - type: main_score
      value: 11.787
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB ArguAna (default)
      revision: c22ab2a51041ffd869aaddef7af8d8215647e41a
      split: test
      type: mteb/arguana
    metrics:
    - type: ndcg_at_1
      value: 33.642
    - type: ndcg_at_3
      value: 48.825
    - type: ndcg_at_5
      value: 53.689
    - type: ndcg_at_10
      value: 58.401
    - type: ndcg_at_20
      value: 60.78
    - type: ndcg_at_100
      value: 61.57
    - type: ndcg_at_1000
      value: 61.608
    - type: map_at_1
      value: 33.642
    - type: map_at_3
      value: 45.057
    - type: map_at_5
      value: 47.774
    - type: map_at_10
      value: 49.716
    - type: map_at_20
      value: 50.400999999999996
    - type: map_at_100
      value: 50.519000000000005
    - type: map_at_1000
      value: 50.52100000000001
    - type: recall_at_1
      value: 33.642
    - type: recall_at_3
      value: 59.744
    - type: recall_at_5
      value: 71.479
    - type: recall_at_10
      value: 86.06
    - type: recall_at_20
      value: 95.235
    - type: recall_at_100
      value: 99.36
    - type: recall_at_1000
      value: 99.644
    - type: precision_at_1
      value: 33.642
    - type: precision_at_3
      value: 19.915
    - type: precision_at_5
      value: 14.296000000000001
    - type: precision_at_10
      value: 8.606
    - type: precision_at_20
      value: 4.7620000000000005
    - type: precision_at_100
      value: 0.9939999999999999
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 34.495
    - type: mrr_at_3
      value: 45.2821
    - type: mrr_at_5
      value: 48.1128
    - type: mrr_at_10
      value: 50.036199999999994
    - type: mrr_at_20
      value: 50.7172
    - type: mrr_at_100
      value: 50.83259999999999
    - type: mrr_at_1000
      value: 50.8343
    - type: nauc_ndcg_at_1_max
      value: -11.838999999999999
    - type: nauc_ndcg_at_1_std
      value: -11.8923
    - type: nauc_ndcg_at_1_diff1
      value: 18.2163
    - type: nauc_ndcg_at_3_max
      value: -11.6655
    - type: nauc_ndcg_at_3_std
      value: -12.2408
    - type: nauc_ndcg_at_3_diff1
      value: 12.4326
    - type: nauc_ndcg_at_5_max
      value: -11.2332
    - type: nauc_ndcg_at_5_std
      value: -10.99
    - type: nauc_ndcg_at_5_diff1
      value: 11.4272
    - type: nauc_ndcg_at_10_max
      value: -9.7581
    - type: nauc_ndcg_at_10_std
      value: -10.6279
    - type: nauc_ndcg_at_10_diff1
      value: 12.3219
    - type: nauc_ndcg_at_20_max
      value: -9.070300000000001
    - type: nauc_ndcg_at_20_std
      value: -10.4367
    - type: nauc_ndcg_at_20_diff1
      value: 13.5332
    - type: nauc_ndcg_at_100_max
      value: -10.281
    - type: nauc_ndcg_at_100_std
      value: -10.8575
    - type: nauc_ndcg_at_100_diff1
      value: 13.583899999999998
    - type: nauc_ndcg_at_1000_max
      value: -10.4108
    - type: nauc_ndcg_at_1000_std
      value: -10.9358
    - type: nauc_ndcg_at_1000_diff1
      value: 13.553200000000002
    - type: nauc_map_at_1_max
      value: -11.838999999999999
    - type: nauc_map_at_1_std
      value: -11.8923
    - type: nauc_map_at_1_diff1
      value: 18.2163
    - type: nauc_map_at_3_max
      value: -11.6502
    - type: nauc_map_at_3_std
      value: -12.0988
    - type: nauc_map_at_3_diff1
      value: 13.7581
    - type: nauc_map_at_5_max
      value: -11.345600000000001
    - type: nauc_map_at_5_std
      value: -11.4327
    - type: nauc_map_at_5_diff1
      value: 13.3246
    - type: nauc_map_at_10_max
      value: -10.8652
    - type: nauc_map_at_10_std
      value: -11.3476
    - type: nauc_map_at_10_diff1
      value: 13.7353
    - type: nauc_map_at_20_max
      value: -10.7273
    - type: nauc_map_at_20_std
      value: -11.309800000000001
    - type: nauc_map_at_20_diff1
      value: 14.0429
    - type: nauc_map_at_100_max
      value: -10.8833
    - type: nauc_map_at_100_std
      value: -11.372
    - type: nauc_map_at_100_diff1
      value: 14.0638
    - type: nauc_map_at_1000_max
      value: -10.8878
    - type: nauc_map_at_1000_std
      value: -11.3746
    - type: nauc_map_at_1000_diff1
      value: 14.062
    - type: nauc_recall_at_1_max
      value: -11.838999999999999
    - type: nauc_recall_at_1_std
      value: -11.8923
    - type: nauc_recall_at_1_diff1
      value: 18.2163
    - type: nauc_recall_at_3_max
      value: -11.739099999999999
    - type: nauc_recall_at_3_std
      value: -12.7062
    - type: nauc_recall_at_3_diff1
      value: 8.3694
    - type: nauc_recall_at_5_max
      value: -10.8863
    - type: nauc_recall_at_5_std
      value: -9.1183
    - type: nauc_recall_at_5_diff1
      value: 4.1094
    - type: nauc_recall_at_10_max
      value: -0.9124
    - type: nauc_recall_at_10_std
      value: -4.971
    - type: nauc_recall_at_10_diff1
      value: 3.4779999999999998
    - type: nauc_recall_at_20_max
      value: 29.0035
    - type: nauc_recall_at_20_std
      value: 8.7987
    - type: nauc_recall_at_20_diff1
      value: 11.932
    - type: nauc_recall_at_100_max
      value: 42.377700000000004
    - type: nauc_recall_at_100_std
      value: 55.2136
    - type: nauc_recall_at_100_diff1
      value: 3.1033999999999997
    - type: nauc_recall_at_1000_max
      value: 19.053700000000003
    - type: nauc_recall_at_1000_std
      value: 67.9828
    - type: nauc_recall_at_1000_diff1
      value: -17.644399999999997
    - type: nauc_precision_at_1_max
      value: -11.838999999999999
    - type: nauc_precision_at_1_std
      value: -11.8923
    - type: nauc_precision_at_1_diff1
      value: 18.2163
    - type: nauc_precision_at_3_max
      value: -11.739099999999999
    - type: nauc_precision_at_3_std
      value: -12.7062
    - type: nauc_precision_at_3_diff1
      value: 8.3694
    - type: nauc_precision_at_5_max
      value: -10.8863
    - type: nauc_precision_at_5_std
      value: -9.1183
    - type: nauc_precision_at_5_diff1
      value: 4.1094
    - type: nauc_precision_at_10_max
      value: -0.9124
    - type: nauc_precision_at_10_std
      value: -4.971
    - type: nauc_precision_at_10_diff1
      value: 3.4779999999999998
    - type: nauc_precision_at_20_max
      value: 29.0035
    - type: nauc_precision_at_20_std
      value: 8.7987
    - type: nauc_precision_at_20_diff1
      value: 11.932
    - type: nauc_precision_at_100_max
      value: 42.377700000000004
    - type: nauc_precision_at_100_std
      value: 55.2136
    - type: nauc_precision_at_100_diff1
      value: 3.1033999999999997
    - type: nauc_precision_at_1000_max
      value: 19.053700000000003
    - type: nauc_precision_at_1000_std
      value: 67.9828
    - type: nauc_precision_at_1000_diff1
      value: -17.644399999999997
    - type: nauc_mrr_at_1_max
      value: -12.0053
    - type: nauc_mrr_at_1_std
      value: -11.7296
    - type: nauc_mrr_at_1_diff1
      value: 15.7249
    - type: nauc_mrr_at_3_max
      value: -12.965399999999999
    - type: nauc_mrr_at_3_std
      value: -12.197099999999999
    - type: nauc_mrr_at_3_diff1
      value: 11.228200000000001
    - type: nauc_mrr_at_5_max
      value: -12.3171
    - type: nauc_mrr_at_5_std
      value: -11.3562
    - type: nauc_mrr_at_5_diff1
      value: 11.081900000000001
    - type: nauc_mrr_at_10_max
      value: -11.9397
    - type: nauc_mrr_at_10_std
      value: -11.3157
    - type: nauc_mrr_at_10_diff1
      value: 11.3887
    - type: nauc_mrr_at_20_max
      value: -11.8344
    - type: nauc_mrr_at_20_std
      value: -11.269
    - type: nauc_mrr_at_20_diff1
      value: 11.655600000000002
    - type: nauc_mrr_at_100_max
      value: -11.9825
    - type: nauc_mrr_at_100_std
      value: -11.3178
    - type: nauc_mrr_at_100_diff1
      value: 11.6519
    - type: nauc_mrr_at_1000_max
      value: -11.9871
    - type: nauc_mrr_at_1000_std
      value: -11.3205
    - type: nauc_mrr_at_1000_diff1
      value: 11.6499
    - type: main_score
      value: 58.401
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB ArxivClusteringP2P (default)
      revision: a122ad7f3f0291bf49cc6f4d32aa80929df69d5d
      split: test
      type: mteb/arxiv-clustering-p2p
    metrics:
    - type: v_measure
      value: 48.3018
    - type: v_measure_std
      value: 13.845199999999998
    - type: main_score
      value: 48.3018
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB ArxivClusteringS2S (default)
      revision: f910caf1a6075f7329cdf8c1a6135696f37dbd53
      split: test
      type: mteb/arxiv-clustering-s2s
    metrics:
    - type: v_measure
      value: 44.837900000000005
    - type: v_measure_std
      value: 14.089599999999999
    - type: main_score
      value: 44.837900000000005
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB AskUbuntuDupQuestions (default)
      revision: 2000358ca161889fa9c082cb41daa8dcfb161a54
      split: test
      type: mteb/askubuntudupquestions-reranking
    metrics:
    - type: map
      value: 66.4838
    - type: mrr
      value: 79.3195
    - type: nAUC_map_max
      value: 23.2658
    - type: nAUC_map_std
      value: 17.5795
    - type: nAUC_map_diff1
      value: 11.5539
    - type: nAUC_mrr_max
      value: 35.565400000000004
    - type: nAUC_mrr_std
      value: 23.7189
    - type: nAUC_mrr_diff1
      value: 15.962299999999999
    - type: main_score
      value: 66.4838
    task:
      type: Reranking
  - dataset:
      config: default
      name: MTEB BIOSSES (default)
      revision: d3fb88f8f02e40887cd149695127462bbcf29b4a
      split: test
      type: mteb/biosses-sts
    metrics:
    - type: pearson
      value: 90.1203
    - type: spearman
      value: 87.8424
    - type: cosine_pearson
      value: 90.1203
    - type: cosine_spearman
      value: 87.8424
    - type: manhattan_pearson
      value: 88.1164
    - type: manhattan_spearman
      value: 87.752
    - type: euclidean_pearson
      value: 88.3146
    - type: euclidean_spearman
      value: 87.8424
    - type: main_score
      value: 87.8424
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB Banking77Classification (default)
      revision: 0fd18e25b25c072e09e0d92ab615fda904d66300
      split: test
      type: mteb/banking77
    metrics:
    - type: accuracy
      value: 77.9156
    - type: f1
      value: 76.9641
    - type: f1_weighted
      value: 76.9641
    - type: main_score
      value: 77.9156
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB BiorxivClusteringP2P (default)
      revision: 65b79d1d13f80053f67aca9498d9402c2d9f1f40
      split: test
      type: mteb/biorxiv-clustering-p2p
    metrics:
    - type: v_measure
      value: 38.3582
    - type: v_measure_std
      value: 1.1436
    - type: main_score
      value: 38.3582
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB BiorxivClusteringS2S (default)
      revision: 258694dd0231531bc1fd9de6ceb52a0853c6d908
      split: test
      type: mteb/biorxiv-clustering-s2s
    metrics:
    - type: v_measure
      value: 36.2911
    - type: v_measure_std
      value: 0.44339999999999996
    - type: main_score
      value: 36.2911
    task:
      type: Clustering
  - dataset:
      config: python
      name: MTEB COIRCodeSearchNetRetrieval (python)
      revision: 4adc7bc41202b5c13543c9c886a25f340634dab3
      split: test
      type: CoIR-Retrieval/CodeSearchNet
    metrics:
    - type: ndcg_at_1
      value: 76.351
    - type: ndcg_at_3
      value: 82.116
    - type: ndcg_at_5
      value: 83.231
    - type: ndcg_at_10
      value: 84.301
    - type: ndcg_at_20
      value: 84.83800000000001
    - type: ndcg_at_100
      value: 85.462
    - type: ndcg_at_1000
      value: 85.706
    - type: map_at_1
      value: 76.351
    - type: map_at_3
      value: 80.744
    - type: map_at_5
      value: 81.365
    - type: map_at_10
      value: 81.812
    - type: map_at_20
      value: 81.96
    - type: map_at_100
      value: 82.05
    - type: map_at_1000
      value: 82.06
    - type: recall_at_1
      value: 76.351
    - type: recall_at_3
      value: 86.071
    - type: recall_at_5
      value: 88.765
    - type: recall_at_10
      value: 92.04299999999999
    - type: recall_at_20
      value: 94.16799999999999
    - type: recall_at_100
      value: 97.466
    - type: recall_at_1000
      value: 99.383
    - type: precision_at_1
      value: 76.351
    - type: precision_at_3
      value: 28.689999999999998
    - type: precision_at_5
      value: 17.753
    - type: precision_at_10
      value: 9.203999999999999
    - type: precision_at_20
      value: 4.707999999999999
    - type: precision_at_100
      value: 0.975
    - type: precision_at_1000
      value: 0.099
    - type: mrr_at_1
      value: 76.3507
    - type: mrr_at_3
      value: 80.7436
    - type: mrr_at_5
      value: 81.3647
    - type: mrr_at_10
      value: 81.8121
    - type: mrr_at_20
      value: 81.9598
    - type: mrr_at_100
      value: 82.0504
    - type: mrr_at_1000
      value: 82.0597
    - type: nauc_ndcg_at_1_max
      value: 73.2541
    - type: nauc_ndcg_at_1_std
      value: -0.8352
    - type: nauc_ndcg_at_1_diff1
      value: 85.1422
    - type: nauc_ndcg_at_3_max
      value: 75.9862
    - type: nauc_ndcg_at_3_std
      value: 0.14100000000000001
    - type: nauc_ndcg_at_3_diff1
      value: 82.4674
    - type: nauc_ndcg_at_5_max
      value: 75.7513
    - type: nauc_ndcg_at_5_std
      value: 0.614
    - type: nauc_ndcg_at_5_diff1
      value: 82.2885
    - type: nauc_ndcg_at_10_max
      value: 75.6282
    - type: nauc_ndcg_at_10_std
      value: 0.6251
    - type: nauc_ndcg_at_10_diff1
      value: 82.3616
    - type: nauc_ndcg_at_20_max
      value: 75.7286
    - type: nauc_ndcg_at_20_std
      value: 0.9792000000000001
    - type: nauc_ndcg_at_20_diff1
      value: 82.6106
    - type: nauc_ndcg_at_100_max
      value: 75.58840000000001
    - type: nauc_ndcg_at_100_std
      value: 1.0781
    - type: nauc_ndcg_at_100_diff1
      value: 82.82969999999999
    - type: nauc_ndcg_at_1000_max
      value: 75.4705
    - type: nauc_ndcg_at_1000_std
      value: 0.8326
    - type: nauc_ndcg_at_1000_diff1
      value: 82.889
    - type: nauc_map_at_1_max
      value: 73.2541
    - type: nauc_map_at_1_std
      value: -0.8352
    - type: nauc_map_at_1_diff1
      value: 85.1422
    - type: nauc_map_at_3_max
      value: 75.2756
    - type: nauc_map_at_3_std
      value: -0.145
    - type: nauc_map_at_3_diff1
      value: 83.15780000000001
    - type: nauc_map_at_5_max
      value: 75.1281
    - type: nauc_map_at_5_std
      value: 0.0837
    - type: nauc_map_at_5_diff1
      value: 83.08250000000001
    - type: nauc_map_at_10_max
      value: 75.05579999999999
    - type: nauc_map_at_10_std
      value: 0.068
    - type: nauc_map_at_10_diff1
      value: 83.1206
    - type: nauc_map_at_20_max
      value: 75.0708
    - type: nauc_map_at_20_std
      value: 0.13749999999999998
    - type: nauc_map_at_20_diff1
      value: 83.1861
    - type: nauc_map_at_100_max
      value: 75.0491
    - type: nauc_map_at_100_std
      value: 0.1411
    - type: nauc_map_at_100_diff1
      value: 83.21539999999999
    - type: nauc_map_at_1000_max
      value: 75.04570000000001
    - type: nauc_map_at_1000_std
      value: 0.1359
    - type: nauc_map_at_1000_diff1
      value: 83.2179
    - type: nauc_recall_at_1_max
      value: 73.2541
    - type: nauc_recall_at_1_std
      value: -0.8352
    - type: nauc_recall_at_1_diff1
      value: 85.1422
    - type: nauc_recall_at_3_max
      value: 78.65990000000001
    - type: nauc_recall_at_3_std
      value: 1.2368000000000001
    - type: nauc_recall_at_3_diff1
      value: 79.8732
    - type: nauc_recall_at_5_max
      value: 78.46
    - type: nauc_recall_at_5_std
      value: 3.1027
    - type: nauc_recall_at_5_diff1
      value: 78.7509
    - type: nauc_recall_at_10_max
      value: 78.9542
    - type: nauc_recall_at_10_std
      value: 4.2138
    - type: nauc_recall_at_10_diff1
      value: 77.8697
    - type: nauc_recall_at_20_max
      value: 81.2016
    - type: nauc_recall_at_20_std
      value: 9.092500000000001
    - type: nauc_recall_at_20_diff1
      value: 78.6045
    - type: nauc_recall_at_100_max
      value: 84.5044
    - type: nauc_recall_at_100_std
      value: 22.6368
    - type: nauc_recall_at_100_diff1
      value: 79.553
    - type: nauc_recall_at_1000_max
      value: 91.4393
    - type: nauc_recall_at_1000_std
      value: 44.0261
    - type: nauc_recall_at_1000_diff1
      value: 78.6859
    - type: nauc_precision_at_1_max
      value: 73.2541
    - type: nauc_precision_at_1_std
      value: -0.8352
    - type: nauc_precision_at_1_diff1
      value: 85.1422
    - type: nauc_precision_at_3_max
      value: 78.65990000000001
    - type: nauc_precision_at_3_std
      value: 1.2368000000000001
    - type: nauc_precision_at_3_diff1
      value: 79.8732
    - type: nauc_precision_at_5_max
      value: 78.46
    - type: nauc_precision_at_5_std
      value: 3.1027
    - type: nauc_precision_at_5_diff1
      value: 78.7509
    - type: nauc_precision_at_10_max
      value: 78.9542
    - type: nauc_precision_at_10_std
      value: 4.2138
    - type: nauc_precision_at_10_diff1
      value: 77.8697
    - type: nauc_precision_at_20_max
      value: 81.2016
    - type: nauc_precision_at_20_std
      value: 9.092500000000001
    - type: nauc_precision_at_20_diff1
      value: 78.6045
    - type: nauc_precision_at_100_max
      value: 84.5044
    - type: nauc_precision_at_100_std
      value: 22.6368
    - type: nauc_precision_at_100_diff1
      value: 79.553
    - type: nauc_precision_at_1000_max
      value: 91.4393
    - type: nauc_precision_at_1000_std
      value: 44.0261
    - type: nauc_precision_at_1000_diff1
      value: 78.6859
    - type: nauc_mrr_at_1_max
      value: 73.2541
    - type: nauc_mrr_at_1_std
      value: -0.8352
    - type: nauc_mrr_at_1_diff1
      value: 85.1422
    - type: nauc_mrr_at_3_max
      value: 75.2756
    - type: nauc_mrr_at_3_std
      value: -0.145
    - type: nauc_mrr_at_3_diff1
      value: 83.15780000000001
    - type: nauc_mrr_at_5_max
      value: 75.1281
    - type: nauc_mrr_at_5_std
      value: 0.0837
    - type: nauc_mrr_at_5_diff1
      value: 83.08250000000001
    - type: nauc_mrr_at_10_max
      value: 75.05579999999999
    - type: nauc_mrr_at_10_std
      value: 0.068
    - type: nauc_mrr_at_10_diff1
      value: 83.1206
    - type: nauc_mrr_at_20_max
      value: 75.0708
    - type: nauc_mrr_at_20_std
      value: 0.13749999999999998
    - type: nauc_mrr_at_20_diff1
      value: 83.1861
    - type: nauc_mrr_at_100_max
      value: 75.0491
    - type: nauc_mrr_at_100_std
      value: 0.1411
    - type: nauc_mrr_at_100_diff1
      value: 83.21539999999999
    - type: nauc_mrr_at_1000_max
      value: 75.04570000000001
    - type: nauc_mrr_at_1000_std
      value: 0.1359
    - type: nauc_mrr_at_1000_diff1
      value: 83.2179
    - type: main_score
      value: 84.301
    task:
      type: Retrieval
  - dataset:
      config: javascript
      name: MTEB COIRCodeSearchNetRetrieval (javascript)
      revision: 4adc7bc41202b5c13543c9c886a25f340634dab3
      split: test
      type: CoIR-Retrieval/CodeSearchNet
    metrics:
    - type: ndcg_at_1
      value: 34.154
    - type: ndcg_at_3
      value: 41.637
    - type: ndcg_at_5
      value: 43.775
    - type: ndcg_at_10
      value: 46.093
    - type: ndcg_at_20
      value: 47.659
    - type: ndcg_at_100
      value: 49.975
    - type: ndcg_at_1000
      value: 51.652
    - type: map_at_1
      value: 34.154
    - type: map_at_3
      value: 39.811
    - type: map_at_5
      value: 40.996
    - type: map_at_10
      value: 41.945
    - type: map_at_20
      value: 42.375
    - type: map_at_100
      value: 42.693999999999996
    - type: map_at_1000
      value: 42.752
    - type: recall_at_1
      value: 34.154
    - type: recall_at_3
      value: 46.916000000000004
    - type: recall_at_5
      value: 52.112
    - type: recall_at_10
      value: 59.313
    - type: recall_at_20
      value: 65.512
    - type: recall_at_100
      value: 78.001
    - type: recall_at_1000
      value: 91.49199999999999
    - type: precision_at_1
      value: 34.154
    - type: precision_at_3
      value: 15.639
    - type: precision_at_5
      value: 10.421999999999999
    - type: precision_at_10
      value: 5.931
    - type: precision_at_20
      value: 3.276
    - type: precision_at_100
      value: 0.7799999999999999
    - type: precision_at_1000
      value: 0.091
    - type: mrr_at_1
      value: 34.153800000000004
    - type: mrr_at_3
      value: 39.8106
    - type: mrr_at_5
      value: 40.995599999999996
    - type: mrr_at_10
      value: 41.9454
    - type: mrr_at_20
      value: 42.375099999999996
    - type: mrr_at_100
      value: 42.6943
    - type: mrr_at_1000
      value: 42.7521
    - type: nauc_ndcg_at_1_max
      value: 43.9354
    - type: nauc_ndcg_at_1_std
      value: -3.6563
    - type: nauc_ndcg_at_1_diff1
      value: 63.9034
    - type: nauc_ndcg_at_3_max
      value: 45.9224
    - type: nauc_ndcg_at_3_std
      value: -1.1915
    - type: nauc_ndcg_at_3_diff1
      value: 56.65599999999999
    - type: nauc_ndcg_at_5_max
      value: 45.7943
    - type: nauc_ndcg_at_5_std
      value: -0.7263000000000001
    - type: nauc_ndcg_at_5_diff1
      value: 55.4796
    - type: nauc_ndcg_at_10_max
      value: 45.4291
    - type: nauc_ndcg_at_10_std
      value: 0.12290000000000001
    - type: nauc_ndcg_at_10_diff1
      value: 54.7952
    - type: nauc_ndcg_at_20_max
      value: 45.7072
    - type: nauc_ndcg_at_20_std
      value: 1.3283
    - type: nauc_ndcg_at_20_diff1
      value: 54.8465
    - type: nauc_ndcg_at_100_max
      value: 45.8073
    - type: nauc_ndcg_at_100_std
      value: 1.8653
    - type: nauc_ndcg_at_100_diff1
      value: 54.9886
    - type: nauc_ndcg_at_1000_max
      value: 45.5983
    - type: nauc_ndcg_at_1000_std
      value: 1.2590999999999999
    - type: nauc_ndcg_at_1000_diff1
      value: 55.374500000000005
    - type: nauc_map_at_1_max
      value: 43.9354
    - type: nauc_map_at_1_std
      value: -3.6563
    - type: nauc_map_at_1_diff1
      value: 63.9034
    - type: nauc_map_at_3_max
      value: 45.4465
    - type: nauc_map_at_3_std
      value: -1.7909000000000002
    - type: nauc_map_at_3_diff1
      value: 58.3822
    - type: nauc_map_at_5_max
      value: 45.3588
    - type: nauc_map_at_5_std
      value: -1.5449
    - type: nauc_map_at_5_diff1
      value: 57.737
    - type: nauc_map_at_10_max
      value: 45.2115
    - type: nauc_map_at_10_std
      value: -1.2034
    - type: nauc_map_at_10_diff1
      value: 57.4859
    - type: nauc_map_at_20_max
      value: 45.29
    - type: nauc_map_at_20_std
      value: -0.8769000000000001
    - type: nauc_map_at_20_diff1
      value: 57.510099999999994
    - type: nauc_map_at_100_max
      value: 45.2905
    - type: nauc_map_at_100_std
      value: -0.8298
    - type: nauc_map_at_100_diff1
      value: 57.5373
    - type: nauc_map_at_1000_max
      value: 45.2866
    - type: nauc_map_at_1000_std
      value: -0.8453
    - type: nauc_map_at_1000_diff1
      value: 57.550000000000004
    - type: nauc_recall_at_1_max
      value: 43.9354
    - type: nauc_recall_at_1_std
      value: -3.6563
    - type: nauc_recall_at_1_diff1
      value: 63.9034
    - type: nauc_recall_at_3_max
      value: 47.2962
    - type: nauc_recall_at_3_std
      value: 0.542
    - type: nauc_recall_at_3_diff1
      value: 51.6782
    - type: nauc_recall_at_5_max
      value: 47.0822
    - type: nauc_recall_at_5_std
      value: 1.7794999999999999
    - type: nauc_recall_at_5_diff1
      value: 48.634100000000004
    - type: nauc_recall_at_10_max
      value: 45.9453
    - type: nauc_recall_at_10_std
      value: 4.7773
    - type: nauc_recall_at_10_diff1
      value: 45.778600000000004
    - type: nauc_recall_at_20_max
      value: 47.232400000000005
    - type: nauc_recall_at_20_std
      value: 10.7522
    - type: nauc_recall_at_20_diff1
      value: 45.029599999999995
    - type: nauc_recall_at_100_max
      value: 48.937799999999996
    - type: nauc_recall_at_100_std
      value: 19.4035
    - type: nauc_recall_at_100_diff1
      value: 42.388
    - type: nauc_recall_at_1000_max
      value: 46.494099999999996
    - type: nauc_recall_at_1000_std
      value: 24.532
    - type: nauc_recall_at_1000_diff1
      value: 36.9281
    - type: nauc_precision_at_1_max
      value: 43.9354
    - type: nauc_precision_at_1_std
      value: -3.6563
    - type: nauc_precision_at_1_diff1
      value: 63.9034
    - type: nauc_precision_at_3_max
      value: 47.2962
    - type: nauc_precision_at_3_std
      value: 0.542
    - type: nauc_precision_at_3_diff1
      value: 51.6782
    - type: nauc_precision_at_5_max
      value: 47.0822
    - type: nauc_precision_at_5_std
      value: 1.7794999999999999
    - type: nauc_precision_at_5_diff1
      value: 48.634100000000004
    - type: nauc_precision_at_10_max
      value: 45.9453
    - type: nauc_precision_at_10_std
      value: 4.7773
    - type: nauc_precision_at_10_diff1
      value: 45.778600000000004
    - type: nauc_precision_at_20_max
      value: 47.232400000000005
    - type: nauc_precision_at_20_std
      value: 10.7522
    - type: nauc_precision_at_20_diff1
      value: 45.029599999999995
    - type: nauc_precision_at_100_max
      value: 48.937799999999996
    - type: nauc_precision_at_100_std
      value: 19.4035
    - type: nauc_precision_at_100_diff1
      value: 42.388
    - type: nauc_precision_at_1000_max
      value: 46.494099999999996
    - type: nauc_precision_at_1000_std
      value: 24.532
    - type: nauc_precision_at_1000_diff1
      value: 36.9281
    - type: nauc_mrr_at_1_max
      value: 43.9354
    - type: nauc_mrr_at_1_std
      value: -3.6563
    - type: nauc_mrr_at_1_diff1
      value: 63.9034
    - type: nauc_mrr_at_3_max
      value: 45.4465
    - type: nauc_mrr_at_3_std
      value: -1.7909000000000002
    - type: nauc_mrr_at_3_diff1
      value: 58.3822
    - type: nauc_mrr_at_5_max
      value: 45.3588
    - type: nauc_mrr_at_5_std
      value: -1.5449
    - type: nauc_mrr_at_5_diff1
      value: 57.737
    - type: nauc_mrr_at_10_max
      value: 45.2115
    - type: nauc_mrr_at_10_std
      value: -1.2034
    - type: nauc_mrr_at_10_diff1
      value: 57.4859
    - type: nauc_mrr_at_20_max
      value: 45.29
    - type: nauc_mrr_at_20_std
      value: -0.8769000000000001
    - type: nauc_mrr_at_20_diff1
      value: 57.510099999999994
    - type: nauc_mrr_at_100_max
      value: 45.2906
    - type: nauc_mrr_at_100_std
      value: -0.8297000000000001
    - type: nauc_mrr_at_100_diff1
      value: 57.5373
    - type: nauc_mrr_at_1000_max
      value: 45.2866
    - type: nauc_mrr_at_1000_std
      value: -0.8452
    - type: nauc_mrr_at_1000_diff1
      value: 57.550000000000004
    - type: main_score
      value: 46.093
    task:
      type: Retrieval
  - dataset:
      config: go
      name: MTEB COIRCodeSearchNetRetrieval (go)
      revision: 4adc7bc41202b5c13543c9c886a25f340634dab3
      split: test
      type: CoIR-Retrieval/CodeSearchNet
    metrics:
    - type: ndcg_at_1
      value: 43.105
    - type: ndcg_at_3
      value: 52.758
    - type: ndcg_at_5
      value: 55.284
    - type: ndcg_at_10
      value: 57.557
    - type: ndcg_at_20
      value: 58.885
    - type: ndcg_at_100
      value: 60.803
    - type: ndcg_at_1000
      value: 61.855000000000004
    - type: map_at_1
      value: 43.105
    - type: map_at_3
      value: 50.38399999999999
    - type: map_at_5
      value: 51.783
    - type: map_at_10
      value: 52.727999999999994
    - type: map_at_20
      value: 53.095000000000006
    - type: map_at_100
      value: 53.361999999999995
    - type: map_at_1000
      value: 53.400000000000006
    - type: recall_at_1
      value: 43.105
    - type: recall_at_3
      value: 59.628
    - type: recall_at_5
      value: 65.77199999999999
    - type: recall_at_10
      value: 72.765
    - type: recall_at_20
      value: 77.998
    - type: recall_at_100
      value: 88.31599999999999
    - type: recall_at_1000
      value: 96.71300000000001
    - type: precision_at_1
      value: 43.105
    - type: precision_at_3
      value: 19.875999999999998
    - type: precision_at_5
      value: 13.154
    - type: precision_at_10
      value: 7.277
    - type: precision_at_20
      value: 3.9
    - type: precision_at_100
      value: 0.8829999999999999
    - type: precision_at_1000
      value: 0.097
    - type: mrr_at_1
      value: 43.1051
    - type: mrr_at_3
      value: 50.3837
    - type: mrr_at_5
      value: 51.783
    - type: mrr_at_10
      value: 52.727900000000005
    - type: mrr_at_20
      value: 53.0949
    - type: mrr_at_100
      value: 53.3622
    - type: mrr_at_1000
      value: 53.400000000000006
    - type: nauc_ndcg_at_1_max
      value: 37.3169
    - type: nauc_ndcg_at_1_std
      value: -2.3253
    - type: nauc_ndcg_at_1_diff1
      value: 60.0465
    - type: nauc_ndcg_at_3_max
      value: 38.2665
    - type: nauc_ndcg_at_3_std
      value: -2.7671
    - type: nauc_ndcg_at_3_diff1
      value: 54.8964
    - type: nauc_ndcg_at_5_max
      value: 38.4714
    - type: nauc_ndcg_at_5_std
      value: -2.7024
    - type: nauc_ndcg_at_5_diff1
      value: 54.207899999999995
    - type: nauc_ndcg_at_10_max
      value: 38.4099
    - type: nauc_ndcg_at_10_std
      value: -2.5911
    - type: nauc_ndcg_at_10_diff1
      value: 53.9601
    - type: nauc_ndcg_at_20_max
      value: 38.406400000000005
    - type: nauc_ndcg_at_20_std
      value: -2.3428
    - type: nauc_ndcg_at_20_diff1
      value: 54.008
    - type: nauc_ndcg_at_100_max
      value: 38.485
    - type: nauc_ndcg_at_100_std
      value: -2.0368
    - type: nauc_ndcg_at_100_diff1
      value: 54.238299999999995
    - type: nauc_ndcg_at_1000_max
      value: 38.5112
    - type: nauc_ndcg_at_1000_std
      value: -2.1126
    - type: nauc_ndcg_at_1000_diff1
      value: 54.6965
    - type: nauc_map_at_1_max
      value: 37.3169
    - type: nauc_map_at_1_std
      value: -2.3253
    - type: nauc_map_at_1_diff1
      value: 60.0465
    - type: nauc_map_at_3_max
      value: 38.0384
    - type: nauc_map_at_3_std
      value: -2.6754
    - type: nauc_map_at_3_diff1
      value: 56.137899999999995
    - type: nauc_map_at_5_max
      value: 38.1522
    - type: nauc_map_at_5_std
      value: -2.6406
    - type: nauc_map_at_5_diff1
      value: 55.80310000000001
    - type: nauc_map_at_10_max
      value: 38.128299999999996
    - type: nauc_map_at_10_std
      value: -2.5891
    - type: nauc_map_at_10_diff1
      value: 55.7289
    - type: nauc_map_at_20_max
      value: 38.128
    - type: nauc_map_at_20_std
      value: -2.5267
    - type: nauc_map_at_20_diff1
      value: 55.758700000000005
    - type: nauc_map_at_100_max
      value: 38.1402
    - type: nauc_map_at_100_std
      value: -2.4964
    - type: nauc_map_at_100_diff1
      value: 55.80159999999999
    - type: nauc_map_at_1000_max
      value: 38.1428
    - type: nauc_map_at_1000_std
      value: -2.4949
    - type: nauc_map_at_1000_diff1
      value: 55.8162
    - type: nauc_recall_at_1_max
      value: 37.3169
    - type: nauc_recall_at_1_std
      value: -2.3253
    - type: nauc_recall_at_1_diff1
      value: 60.0465
    - type: nauc_recall_at_3_max
      value: 38.9708
    - type: nauc_recall_at_3_std
      value: -3.0438
    - type: nauc_recall_at_3_diff1
      value: 51.0597
    - type: nauc_recall_at_5_max
      value: 39.5722
    - type: nauc_recall_at_5_std
      value: -2.8886
    - type: nauc_recall_at_5_diff1
      value: 48.6862
    - type: nauc_recall_at_10_max
      value: 39.494
    - type: nauc_recall_at_10_std
      value: -2.5299
    - type: nauc_recall_at_10_diff1
      value: 46.75
    - type: nauc_recall_at_20_max
      value: 39.6388
    - type: nauc_recall_at_20_std
      value: -1.0715999999999999
    - type: nauc_recall_at_20_diff1
      value: 45.6381
    - type: nauc_recall_at_100_max
      value: 41.4357
    - type: nauc_recall_at_100_std
      value: 4.1693
    - type: nauc_recall_at_100_diff1
      value: 42.2097
    - type: nauc_recall_at_1000_max
      value: 49.2056
    - type: nauc_recall_at_1000_std
      value: 12.2387
    - type: nauc_recall_at_1000_diff1
      value: 42.7371
    - type: nauc_precision_at_1_max
      value: 37.3169
    - type: nauc_precision_at_1_std
      value: -2.3253
    - type: nauc_precision_at_1_diff1
      value: 60.0465
    - type: nauc_precision_at_3_max
      value: 38.9708
    - type: nauc_precision_at_3_std
      value: -3.0438
    - type: nauc_precision_at_3_diff1
      value: 51.0597
    - type: nauc_precision_at_5_max
      value: 39.5722
    - type: nauc_precision_at_5_std
      value: -2.8886
    - type: nauc_precision_at_5_diff1
      value: 48.6862
    - type: nauc_precision_at_10_max
      value: 39.494
    - type: nauc_precision_at_10_std
      value: -2.5299
    - type: nauc_precision_at_10_diff1
      value: 46.75
    - type: nauc_precision_at_20_max
      value: 39.6388
    - type: nauc_precision_at_20_std
      value: -1.0715999999999999
    - type: nauc_precision_at_20_diff1
      value: 45.6381
    - type: nauc_precision_at_100_max
      value: 41.4357
    - type: nauc_precision_at_100_std
      value: 4.1693
    - type: nauc_precision_at_100_diff1
      value: 42.2097
    - type: nauc_precision_at_1000_max
      value: 49.2056
    - type: nauc_precision_at_1000_std
      value: 12.2387
    - type: nauc_precision_at_1000_diff1
      value: 42.7371
    - type: nauc_mrr_at_1_max
      value: 37.3169
    - type: nauc_mrr_at_1_std
      value: -2.3253
    - type: nauc_mrr_at_1_diff1
      value: 60.0465
    - type: nauc_mrr_at_3_max
      value: 38.0384
    - type: nauc_mrr_at_3_std
      value: -2.6754
    - type: nauc_mrr_at_3_diff1
      value: 56.137899999999995
    - type: nauc_mrr_at_5_max
      value: 38.1522
    - type: nauc_mrr_at_5_std
      value: -2.6406
    - type: nauc_mrr_at_5_diff1
      value: 55.80310000000001
    - type: nauc_mrr_at_10_max
      value: 38.128299999999996
    - type: nauc_mrr_at_10_std
      value: -2.5891
    - type: nauc_mrr_at_10_diff1
      value: 55.7289
    - type: nauc_mrr_at_20_max
      value: 38.128
    - type: nauc_mrr_at_20_std
      value: -2.5267
    - type: nauc_mrr_at_20_diff1
      value: 55.758700000000005
    - type: nauc_mrr_at_100_max
      value: 38.1402
    - type: nauc_mrr_at_100_std
      value: -2.4964
    - type: nauc_mrr_at_100_diff1
      value: 55.80159999999999
    - type: nauc_mrr_at_1000_max
      value: 38.1428
    - type: nauc_mrr_at_1000_std
      value: -2.4949
    - type: nauc_mrr_at_1000_diff1
      value: 55.8162
    - type: main_score
      value: 57.557
    task:
      type: Retrieval
  - dataset:
      config: ruby
      name: MTEB COIRCodeSearchNetRetrieval (ruby)
      revision: 4adc7bc41202b5c13543c9c886a25f340634dab3
      split: test
      type: CoIR-Retrieval/CodeSearchNet
    metrics:
    - type: ndcg_at_1
      value: 33.466
    - type: ndcg_at_3
      value: 41.611
    - type: ndcg_at_5
      value: 44.41
    - type: ndcg_at_10
      value: 46.878
    - type: ndcg_at_20
      value: 48.548
    - type: ndcg_at_100
      value: 51.004000000000005
    - type: ndcg_at_1000
      value: 52.564
    - type: map_at_1
      value: 33.466
    - type: map_at_3
      value: 39.650999999999996
    - type: map_at_5
      value: 41.217
    - type: map_at_10
      value: 42.225
    - type: map_at_20
      value: 42.687000000000005
    - type: map_at_100
      value: 43.025000000000006
    - type: map_at_1000
      value: 43.082
    - type: recall_at_1
      value: 33.466
    - type: recall_at_3
      value: 47.264
    - type: recall_at_5
      value: 54.005
    - type: recall_at_10
      value: 61.697
    - type: recall_at_20
      value: 68.279
    - type: recall_at_100
      value: 81.523
    - type: recall_at_1000
      value: 93.973
    - type: precision_at_1
      value: 33.466
    - type: precision_at_3
      value: 15.754999999999999
    - type: precision_at_5
      value: 10.801
    - type: precision_at_10
      value: 6.17
    - type: precision_at_20
      value: 3.4139999999999997
    - type: precision_at_100
      value: 0.815
    - type: precision_at_1000
      value: 0.094
    - type: mrr_at_1
      value: 33.4655
    - type: mrr_at_3
      value: 39.6511
    - type: mrr_at_5
      value: 41.2173
    - type: mrr_at_10
      value: 42.2253
    - type: mrr_at_20
      value: 42.686800000000005
    - type: mrr_at_100
      value: 43.025000000000006
    - type: mrr_at_1000
      value: 43.0818
    - type: nauc_ndcg_at_1_max
      value: 45.789699999999996
    - type: nauc_ndcg_at_1_std
      value: -4.9502999999999995
    - type: nauc_ndcg_at_1_diff1
      value: 54.9067
    - type: nauc_ndcg_at_3_max
      value: 44.473800000000004
    - type: nauc_ndcg_at_3_std
      value: -2.9877000000000002
    - type: nauc_ndcg_at_3_diff1
      value: 48.611599999999996
    - type: nauc_ndcg_at_5_max
      value: 44.048300000000005
    - type: nauc_ndcg_at_5_std
      value: -2.4233000000000002
    - type: nauc_ndcg_at_5_diff1
      value: 46.6638
    - type: nauc_ndcg_at_10_max
      value: 42.9816
    - type: nauc_ndcg_at_10_std
      value: -1.8901000000000001
    - type: nauc_ndcg_at_10_diff1
      value: 45.9046
    - type: nauc_ndcg_at_20_max
      value: 42.7803
    - type: nauc_ndcg_at_20_std
      value: -1.2547000000000001
    - type: nauc_ndcg_at_20_diff1
      value: 45.305
    - type: nauc_ndcg_at_100_max
      value: 42.918
    - type: nauc_ndcg_at_100_std
      value: -0.6534
    - type: nauc_ndcg_at_100_diff1
      value: 45.6519
    - type: nauc_ndcg_at_1000_max
      value: 43.0112
    - type: nauc_ndcg_at_1000_std
      value: -1.1447
    - type: nauc_ndcg_at_1000_diff1
      value: 46.1206
    - type: nauc_map_at_1_max
      value: 45.789699999999996
    - type: nauc_map_at_1_std
      value: -4.9502999999999995
    - type: nauc_map_at_1_diff1
      value: 54.9067
    - type: nauc_map_at_3_max
      value: 44.6443
    - type: nauc_map_at_3_std
      value: -3.4606
    - type: nauc_map_at_3_diff1
      value: 49.9067
    - type: nauc_map_at_5_max
      value: 44.3838
    - type: nauc_map_at_5_std
      value: -3.1638
    - type: nauc_map_at_5_diff1
      value: 48.829899999999995
    - type: nauc_map_at_10_max
      value: 43.9426
    - type: nauc_map_at_10_std
      value: -2.9687
    - type: nauc_map_at_10_diff1
      value: 48.497
    - type: nauc_map_at_20_max
      value: 43.8915
    - type: nauc_map_at_20_std
      value: -2.8005
    - type: nauc_map_at_20_diff1
      value: 48.3597
    - type: nauc_map_at_100_max
      value: 43.8943
    - type: nauc_map_at_100_std
      value: -2.7306
    - type: nauc_map_at_100_diff1
      value: 48.4227
    - type: nauc_map_at_1000_max
      value: 43.8925
    - type: nauc_map_at_1000_std
      value: -2.7446
    - type: nauc_map_at_1000_diff1
      value: 48.4369
    - type: nauc_recall_at_1_max
      value: 45.789699999999996
    - type: nauc_recall_at_1_std
      value: -4.9502999999999995
    - type: nauc_recall_at_1_diff1
      value: 54.9067
    - type: nauc_recall_at_3_max
      value: 44.0419
    - type: nauc_recall_at_3_std
      value: -1.6226
    - type: nauc_recall_at_3_diff1
      value: 44.9647
    - type: nauc_recall_at_5_max
      value: 43.0769
    - type: nauc_recall_at_5_std
      value: -0.1038
    - type: nauc_recall_at_5_diff1
      value: 39.9873
    - type: nauc_recall_at_10_max
      value: 39.4409
    - type: nauc_recall_at_10_std
      value: 2.0126999999999997
    - type: nauc_recall_at_10_diff1
      value: 37.0457
    - type: nauc_recall_at_20_max
      value: 38.0436
    - type: nauc_recall_at_20_std
      value: 5.5206
    - type: nauc_recall_at_20_diff1
      value: 32.9418
    - type: nauc_recall_at_100_max
      value: 37.4262
    - type: nauc_recall_at_100_std
      value: 14.9231
    - type: nauc_recall_at_100_diff1
      value: 29.651100000000003
    - type: nauc_recall_at_1000_max
      value: 33.1185
    - type: nauc_recall_at_1000_std
      value: 23.4133
    - type: nauc_recall_at_1000_diff1
      value: 19.6646
    - type: nauc_precision_at_1_max
      value: 45.789699999999996
    - type: nauc_precision_at_1_std
      value: -4.9502999999999995
    - type: nauc_precision_at_1_diff1
      value: 54.9067
    - type: nauc_precision_at_3_max
      value: 44.0419
    - type: nauc_precision_at_3_std
      value: -1.6226
    - type: nauc_precision_at_3_diff1
      value: 44.9647
    - type: nauc_precision_at_5_max
      value: 43.0769
    - type: nauc_precision_at_5_std
      value: -0.1038
    - type: nauc_precision_at_5_diff1
      value: 39.9873
    - type: nauc_precision_at_10_max
      value: 39.4409
    - type: nauc_precision_at_10_std
      value: 2.0126999999999997
    - type: nauc_precision_at_10_diff1
      value: 37.0457
    - type: nauc_precision_at_20_max
      value: 38.0436
    - type: nauc_precision_at_20_std
      value: 5.5206
    - type: nauc_precision_at_20_diff1
      value: 32.9418
    - type: nauc_precision_at_100_max
      value: 37.4262
    - type: nauc_precision_at_100_std
      value: 14.9231
    - type: nauc_precision_at_100_diff1
      value: 29.651100000000003
    - type: nauc_precision_at_1000_max
      value: 33.1185
    - type: nauc_precision_at_1000_std
      value: 23.4133
    - type: nauc_precision_at_1000_diff1
      value: 19.6646
    - type: nauc_mrr_at_1_max
      value: 45.789699999999996
    - type: nauc_mrr_at_1_std
      value: -4.9502999999999995
    - type: nauc_mrr_at_1_diff1
      value: 54.9067
    - type: nauc_mrr_at_3_max
      value: 44.6443
    - type: nauc_mrr_at_3_std
      value: -3.4606
    - type: nauc_mrr_at_3_diff1
      value: 49.9067
    - type: nauc_mrr_at_5_max
      value: 44.3838
    - type: nauc_mrr_at_5_std
      value: -3.1638
    - type: nauc_mrr_at_5_diff1
      value: 48.829899999999995
    - type: nauc_mrr_at_10_max
      value: 43.9426
    - type: nauc_mrr_at_10_std
      value: -2.9687
    - type: nauc_mrr_at_10_diff1
      value: 48.497
    - type: nauc_mrr_at_20_max
      value: 43.8915
    - type: nauc_mrr_at_20_std
      value: -2.8005
    - type: nauc_mrr_at_20_diff1
      value: 48.3597
    - type: nauc_mrr_at_100_max
      value: 43.8943
    - type: nauc_mrr_at_100_std
      value: -2.7306
    - type: nauc_mrr_at_100_diff1
      value: 48.4227
    - type: nauc_mrr_at_1000_max
      value: 43.8925
    - type: nauc_mrr_at_1000_std
      value: -2.7446
    - type: nauc_mrr_at_1000_diff1
      value: 48.4369
    - type: main_score
      value: 46.878
    task:
      type: Retrieval
  - dataset:
      config: java
      name: MTEB COIRCodeSearchNetRetrieval (java)
      revision: 4adc7bc41202b5c13543c9c886a25f340634dab3
      split: test
      type: CoIR-Retrieval/CodeSearchNet
    metrics:
    - type: ndcg_at_1
      value: 37.91
    - type: ndcg_at_3
      value: 46.022999999999996
    - type: ndcg_at_5
      value: 48.345
    - type: ndcg_at_10
      value: 50.477000000000004
    - type: ndcg_at_20
      value: 51.900999999999996
    - type: ndcg_at_100
      value: 54.01899999999999
    - type: ndcg_at_1000
      value: 55.383
    - type: map_at_1
      value: 37.91
    - type: map_at_3
      value: 44.051
    - type: map_at_5
      value: 45.341
    - type: map_at_10
      value: 46.221000000000004
    - type: map_at_20
      value: 46.613
    - type: map_at_100
      value: 46.902
    - type: map_at_1000
      value: 46.949999999999996
    - type: recall_at_1
      value: 37.91
    - type: recall_at_3
      value: 51.721
    - type: recall_at_5
      value: 57.353
    - type: recall_at_10
      value: 63.943000000000005
    - type: recall_at_20
      value: 69.56599999999999
    - type: recall_at_100
      value: 81.041
    - type: recall_at_1000
      value: 91.995
    - type: precision_at_1
      value: 37.91
    - type: precision_at_3
      value: 17.24
    - type: precision_at_5
      value: 11.471
    - type: precision_at_10
      value: 6.394
    - type: precision_at_20
      value: 3.4779999999999998
    - type: precision_at_100
      value: 0.8099999999999999
    - type: precision_at_1000
      value: 0.092
    - type: mrr_at_1
      value: 37.9096
    - type: mrr_at_3
      value: 44.0514
    - type: mrr_at_5
      value: 45.340799999999994
    - type: mrr_at_10
      value: 46.221000000000004
    - type: mrr_at_20
      value: 46.613
    - type: mrr_at_100
      value: 46.9024
    - type: mrr_at_1000
      value: 46.9499
    - type: nauc_ndcg_at_1_max
      value: 32.0711
    - type: nauc_ndcg_at_1_std
      value: -6.4620999999999995
    - type: nauc_ndcg_at_1_diff1
      value: 57.851200000000006
    - type: nauc_ndcg_at_3_max
      value: 33.6415
    - type: nauc_ndcg_at_3_std
      value: -5.2595
    - type: nauc_ndcg_at_3_diff1
      value: 53.340900000000005
    - type: nauc_ndcg_at_5_max
      value: 33.6962
    - type: nauc_ndcg_at_5_std
      value: -4.3041
    - type: nauc_ndcg_at_5_diff1
      value: 52.137299999999996
    - type: nauc_ndcg_at_10_max
      value: 33.8843
    - type: nauc_ndcg_at_10_std
      value: -3.2363000000000004
    - type: nauc_ndcg_at_10_diff1
      value: 51.5065
    - type: nauc_ndcg_at_20_max
      value: 33.8675
    - type: nauc_ndcg_at_20_std
      value: -2.4443
    - type: nauc_ndcg_at_20_diff1
      value: 51.31790000000001
    - type: nauc_ndcg_at_100_max
      value: 34.2671
    - type: nauc_ndcg_at_100_std
      value: -1.706
    - type: nauc_ndcg_at_100_diff1
      value: 51.3801
    - type: nauc_ndcg_at_1000_max
      value: 34.237
    - type: nauc_ndcg_at_1000_std
      value: -2.0292999999999997
    - type: nauc_ndcg_at_1000_diff1
      value: 51.8196
    - type: nauc_map_at_1_max
      value: 32.0711
    - type: nauc_map_at_1_std
      value: -6.4620999999999995
    - type: nauc_map_at_1_diff1
      value: 57.851200000000006
    - type: nauc_map_at_3_max
      value: 33.271699999999996
    - type: nauc_map_at_3_std
      value: -5.578799999999999
    - type: nauc_map_at_3_diff1
      value: 54.427800000000005
    - type: nauc_map_at_5_max
      value: 33.2962
    - type: nauc_map_at_5_std
      value: -5.063
    - type: nauc_map_at_5_diff1
      value: 53.784
    - type: nauc_map_at_10_max
      value: 33.3553
    - type: nauc_map_at_10_std
      value: -4.6524
    - type: nauc_map_at_10_diff1
      value: 53.5366
    - type: nauc_map_at_20_max
      value: 33.3544
    - type: nauc_map_at_20_std
      value: -4.4497
    - type: nauc_map_at_20_diff1
      value: 53.4978
    - type: nauc_map_at_100_max
      value: 33.4027
    - type: nauc_map_at_100_std
      value: -4.3659
    - type: nauc_map_at_100_diff1
      value: 53.514300000000006
    - type: nauc_map_at_1000_max
      value: 33.4037
    - type: nauc_map_at_1000_std
      value: -4.3740000000000006
    - type: nauc_map_at_1000_diff1
      value: 53.5313
    - type: nauc_recall_at_1_max
      value: 32.0711
    - type: nauc_recall_at_1_std
      value: -6.4620999999999995
    - type: nauc_recall_at_1_diff1
      value: 57.851200000000006
    - type: nauc_recall_at_3_max
      value: 34.7301
    - type: nauc_recall_at_3_std
      value: -4.3033
    - type: nauc_recall_at_3_diff1
      value: 50.129999999999995
    - type: nauc_recall_at_5_max
      value: 34.940599999999996
    - type: nauc_recall_at_5_std
      value: -1.7868
    - type: nauc_recall_at_5_diff1
      value: 46.848
    - type: nauc_recall_at_10_max
      value: 35.8024
    - type: nauc_recall_at_10_std
      value: 2.271
    - type: nauc_recall_at_10_diff1
      value: 44.1597
    - type: nauc_recall_at_20_max
      value: 35.881800000000005
    - type: nauc_recall_at_20_std
      value: 6.7608
    - type: nauc_recall_at_20_diff1
      value: 42.3843
    - type: nauc_recall_at_100_max
      value: 40.5398
    - type: nauc_recall_at_100_std
      value: 17.9288
    - type: nauc_recall_at_100_diff1
      value: 38.9048
    - type: nauc_recall_at_1000_max
      value: 46.6349
    - type: nauc_recall_at_1000_std
      value: 31.1156
    - type: nauc_recall_at_1000_diff1
      value: 36.5951
    - type: nauc_precision_at_1_max
      value: 32.0711
    - type: nauc_precision_at_1_std
      value: -6.4620999999999995
    - type: nauc_precision_at_1_diff1
      value: 57.851200000000006
    - type: nauc_precision_at_3_max
      value: 34.7301
    - type: nauc_precision_at_3_std
      value: -4.3033
    - type: nauc_precision_at_3_diff1
      value: 50.129999999999995
    - type: nauc_precision_at_5_max
      value: 34.940599999999996
    - type: nauc_precision_at_5_std
      value: -1.7868
    - type: nauc_precision_at_5_diff1
      value: 46.848
    - type: nauc_precision_at_10_max
      value: 35.8024
    - type: nauc_precision_at_10_std
      value: 2.271
    - type: nauc_precision_at_10_diff1
      value: 44.1597
    - type: nauc_precision_at_20_max
      value: 35.881800000000005
    - type: nauc_precision_at_20_std
      value: 6.7608
    - type: nauc_precision_at_20_diff1
      value: 42.3843
    - type: nauc_precision_at_100_max
      value: 40.5398
    - type: nauc_precision_at_100_std
      value: 17.9288
    - type: nauc_precision_at_100_diff1
      value: 38.9048
    - type: nauc_precision_at_1000_max
      value: 46.6349
    - type: nauc_precision_at_1000_std
      value: 31.1156
    - type: nauc_precision_at_1000_diff1
      value: 36.5951
    - type: nauc_mrr_at_1_max
      value: 32.0711
    - type: nauc_mrr_at_1_std
      value: -6.4620999999999995
    - type: nauc_mrr_at_1_diff1
      value: 57.851200000000006
    - type: nauc_mrr_at_3_max
      value: 33.271699999999996
    - type: nauc_mrr_at_3_std
      value: -5.578799999999999
    - type: nauc_mrr_at_3_diff1
      value: 54.427800000000005
    - type: nauc_mrr_at_5_max
      value: 33.2962
    - type: nauc_mrr_at_5_std
      value: -5.063
    - type: nauc_mrr_at_5_diff1
      value: 53.784
    - type: nauc_mrr_at_10_max
      value: 33.3553
    - type: nauc_mrr_at_10_std
      value: -4.6524
    - type: nauc_mrr_at_10_diff1
      value: 53.5366
    - type: nauc_mrr_at_20_max
      value: 33.3544
    - type: nauc_mrr_at_20_std
      value: -4.4497
    - type: nauc_mrr_at_20_diff1
      value: 53.4978
    - type: nauc_mrr_at_100_max
      value: 33.4027
    - type: nauc_mrr_at_100_std
      value: -4.3659
    - type: nauc_mrr_at_100_diff1
      value: 53.514300000000006
    - type: nauc_mrr_at_1000_max
      value: 33.4037
    - type: nauc_mrr_at_1000_std
      value: -4.3740000000000006
    - type: nauc_mrr_at_1000_diff1
      value: 53.5313
    - type: main_score
      value: 50.477000000000004
    task:
      type: Retrieval
  - dataset:
      config: php
      name: MTEB COIRCodeSearchNetRetrieval (php)
      revision: 4adc7bc41202b5c13543c9c886a25f340634dab3
      split: test
      type: CoIR-Retrieval/CodeSearchNet
    metrics:
    - type: ndcg_at_1
      value: 32.253
    - type: ndcg_at_3
      value: 40.355999999999995
    - type: ndcg_at_5
      value: 42.85
    - type: ndcg_at_10
      value: 45.217
    - type: ndcg_at_20
      value: 47.13
    - type: ndcg_at_100
      value: 49.683
    - type: ndcg_at_1000
      value: 51.248000000000005
    - type: map_at_1
      value: 32.253
    - type: map_at_3
      value: 38.374
    - type: map_at_5
      value: 39.757999999999996
    - type: map_at_10
      value: 40.731
    - type: map_at_20
      value: 41.254999999999995
    - type: map_at_100
      value: 41.6
    - type: map_at_1000
      value: 41.654
    - type: recall_at_1
      value: 32.253
    - type: recall_at_3
      value: 46.089999999999996
    - type: recall_at_5
      value: 52.141000000000005
    - type: recall_at_10
      value: 59.483
    - type: recall_at_20
      value: 67.054
    - type: recall_at_100
      value: 80.93299999999999
    - type: recall_at_1000
      value: 93.499
    - type: precision_at_1
      value: 32.253
    - type: precision_at_3
      value: 15.363
    - type: precision_at_5
      value: 10.427999999999999
    - type: precision_at_10
      value: 5.9479999999999995
    - type: precision_at_20
      value: 3.3529999999999998
    - type: precision_at_100
      value: 0.8089999999999999
    - type: precision_at_1000
      value: 0.093
    - type: mrr_at_1
      value: 32.2535
    - type: mrr_at_3
      value: 38.3735
    - type: mrr_at_5
      value: 39.7582
    - type: mrr_at_10
      value: 40.7309
    - type: mrr_at_20
      value: 41.254999999999995
    - type: mrr_at_100
      value: 41.6001
    - type: mrr_at_1000
      value: 41.6545
    - type: nauc_ndcg_at_1_max
      value: 29.5043
    - type: nauc_ndcg_at_1_std
      value: -3.8282999999999996
    - type: nauc_ndcg_at_1_diff1
      value: 55.538399999999996
    - type: nauc_ndcg_at_3_max
      value: 30.1745
    - type: nauc_ndcg_at_3_std
      value: -2.6322
    - type: nauc_ndcg_at_3_diff1
      value: 49.4579
    - type: nauc_ndcg_at_5_max
      value: 29.990699999999997
    - type: nauc_ndcg_at_5_std
      value: -2.2249000000000003
    - type: nauc_ndcg_at_5_diff1
      value: 48.5017
    - type: nauc_ndcg_at_10_max
      value: 29.8609
    - type: nauc_ndcg_at_10_std
      value: -1.6362999999999999
    - type: nauc_ndcg_at_10_diff1
      value: 47.7191
    - type: nauc_ndcg_at_20_max
      value: 30.1378
    - type: nauc_ndcg_at_20_std
      value: -0.6985
    - type: nauc_ndcg_at_20_diff1
      value: 47.5359
    - type: nauc_ndcg_at_100_max
      value: 30.5901
    - type: nauc_ndcg_at_100_std
      value: 0.1903
    - type: nauc_ndcg_at_100_diff1
      value: 47.765299999999996
    - type: nauc_ndcg_at_1000_max
      value: 30.607200000000002
    - type: nauc_ndcg_at_1000_std
      value: -0.1485
    - type: nauc_ndcg_at_1000_diff1
      value: 48.3165
    - type: nauc_map_at_1_max
      value: 29.5043
    - type: nauc_map_at_1_std
      value: -3.8282999999999996
    - type: nauc_map_at_1_diff1
      value: 55.538399999999996
    - type: nauc_map_at_3_max
      value: 30.0348
    - type: nauc_map_at_3_std
      value: -2.9402
    - type: nauc_map_at_3_diff1
      value: 50.8128
    - type: nauc_map_at_5_max
      value: 29.9447
    - type: nauc_map_at_5_std
      value: -2.7157
    - type: nauc_map_at_5_diff1
      value: 50.2953
    - type: nauc_map_at_10_max
      value: 29.8929
    - type: nauc_map_at_10_std
      value: -2.4865000000000004
    - type: nauc_map_at_10_diff1
      value: 49.9942
    - type: nauc_map_at_20_max
      value: 29.9564
    - type: nauc_map_at_20_std
      value: -2.2576
    - type: nauc_map_at_20_diff1
      value: 49.961800000000004
    - type: nauc_map_at_100_max
      value: 30.0155
    - type: nauc_map_at_100_std
      value: -2.1527000000000003
    - type: nauc_map_at_100_diff1
      value: 50.00320000000001
    - type: nauc_map_at_1000_max
      value: 30.0156
    - type: nauc_map_at_1000_std
      value: -2.1597999999999997
    - type: nauc_map_at_1000_diff1
      value: 50.019000000000005
    - type: nauc_recall_at_1_max
      value: 29.5043
    - type: nauc_recall_at_1_std
      value: -3.8282999999999996
    - type: nauc_recall_at_1_diff1
      value: 55.538399999999996
    - type: nauc_recall_at_3_max
      value: 30.567
    - type: nauc_recall_at_3_std
      value: -1.7389999999999999
    - type: nauc_recall_at_3_diff1
      value: 45.6079
    - type: nauc_recall_at_5_max
      value: 30.074499999999997
    - type: nauc_recall_at_5_std
      value: -0.7081
    - type: nauc_recall_at_5_diff1
      value: 43.1053
    - type: nauc_recall_at_10_max
      value: 29.644
    - type: nauc_recall_at_10_std
      value: 1.4013
    - type: nauc_recall_at_10_diff1
      value: 40.0676
    - type: nauc_recall_at_20_max
      value: 31.0116
    - type: nauc_recall_at_20_std
      value: 6.3982
    - type: nauc_recall_at_20_diff1
      value: 38.085
    - type: nauc_recall_at_100_max
      value: 35.6387
    - type: nauc_recall_at_100_std
      value: 18.4894
    - type: nauc_recall_at_100_diff1
      value: 35.2692
    - type: nauc_recall_at_1000_max
      value: 44.9874
    - type: nauc_recall_at_1000_std
      value: 36.0452
    - type: nauc_recall_at_1000_diff1
      value: 34.8612
    - type: nauc_precision_at_1_max
      value: 29.5043
    - type: nauc_precision_at_1_std
      value: -3.8282999999999996
    - type: nauc_precision_at_1_diff1
      value: 55.538399999999996
    - type: nauc_precision_at_3_max
      value: 30.567
    - type: nauc_precision_at_3_std
      value: -1.7389999999999999
    - type: nauc_precision_at_3_diff1
      value: 45.6079
    - type: nauc_precision_at_5_max
      value: 30.074499999999997
    - type: nauc_precision_at_5_std
      value: -0.7081
    - type: nauc_precision_at_5_diff1
      value: 43.1053
    - type: nauc_precision_at_10_max
      value: 29.644
    - type: nauc_precision_at_10_std
      value: 1.4013
    - type: nauc_precision_at_10_diff1
      value: 40.0676
    - type: nauc_precision_at_20_max
      value: 31.0116
    - type: nauc_precision_at_20_std
      value: 6.3982
    - type: nauc_precision_at_20_diff1
      value: 38.085
    - type: nauc_precision_at_100_max
      value: 35.6387
    - type: nauc_precision_at_100_std
      value: 18.4894
    - type: nauc_precision_at_100_diff1
      value: 35.2692
    - type: nauc_precision_at_1000_max
      value: 44.9874
    - type: nauc_precision_at_1000_std
      value: 36.0452
    - type: nauc_precision_at_1000_diff1
      value: 34.8612
    - type: nauc_mrr_at_1_max
      value: 29.5043
    - type: nauc_mrr_at_1_std
      value: -3.8282999999999996
    - type: nauc_mrr_at_1_diff1
      value: 55.538399999999996
    - type: nauc_mrr_at_3_max
      value: 30.0348
    - type: nauc_mrr_at_3_std
      value: -2.9402
    - type: nauc_mrr_at_3_diff1
      value: 50.8128
    - type: nauc_mrr_at_5_max
      value: 29.9447
    - type: nauc_mrr_at_5_std
      value: -2.7157
    - type: nauc_mrr_at_5_diff1
      value: 50.2953
    - type: nauc_mrr_at_10_max
      value: 29.8929
    - type: nauc_mrr_at_10_std
      value: -2.4865000000000004
    - type: nauc_mrr_at_10_diff1
      value: 49.9942
    - type: nauc_mrr_at_20_max
      value: 29.9564
    - type: nauc_mrr_at_20_std
      value: -2.2576
    - type: nauc_mrr_at_20_diff1
      value: 49.961800000000004
    - type: nauc_mrr_at_100_max
      value: 30.0155
    - type: nauc_mrr_at_100_std
      value: -2.1527000000000003
    - type: nauc_mrr_at_100_diff1
      value: 50.00320000000001
    - type: nauc_mrr_at_1000_max
      value: 30.0156
    - type: nauc_mrr_at_1000_std
      value: -2.1597999999999997
    - type: nauc_mrr_at_1000_diff1
      value: 50.019000000000005
    - type: main_score
      value: 45.217
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackAndroidRetrieval (default)
      revision: f46a197baaae43b4f621051089b82a364682dfeb
      split: test
      type: mteb/cqadupstack-android
    metrics:
    - type: ndcg_at_1
      value: 45.923
    - type: ndcg_at_3
      value: 51.842999999999996
    - type: ndcg_at_5
      value: 54.257
    - type: ndcg_at_10
      value: 57.667
    - type: ndcg_at_20
      value: 59.516000000000005
    - type: ndcg_at_100
      value: 62.373
    - type: ndcg_at_1000
      value: 63.68000000000001
    - type: map_at_1
      value: 36.964000000000006
    - type: map_at_3
      value: 46.001
    - type: map_at_5
      value: 48.312
    - type: map_at_10
      value: 50.43
    - type: map_at_20
      value: 51.371
    - type: map_at_100
      value: 52.066
    - type: map_at_1000
      value: 52.175000000000004
    - type: recall_at_1
      value: 36.964000000000006
    - type: recall_at_3
      value: 53.654999999999994
    - type: recall_at_5
      value: 60.995999999999995
    - type: recall_at_10
      value: 71.234
    - type: recall_at_20
      value: 77.596
    - type: recall_at_100
      value: 90.42099999999999
    - type: recall_at_1000
      value: 98.29599999999999
    - type: precision_at_1
      value: 45.923
    - type: precision_at_3
      value: 25.369999999999997
    - type: precision_at_5
      value: 18.14
    - type: precision_at_10
      value: 11.315999999999999
    - type: precision_at_20
      value: 6.651999999999999
    - type: precision_at_100
      value: 1.7049999999999998
    - type: precision_at_1000
      value: 0.216
    - type: mrr_at_1
      value: 45.9227
    - type: mrr_at_3
      value: 54.053399999999996
    - type: mrr_at_5
      value: 55.555600000000005
    - type: mrr_at_10
      value: 56.7326
    - type: mrr_at_20
      value: 57.0026
    - type: mrr_at_100
      value: 57.2924
    - type: mrr_at_1000
      value: 57.321299999999994
    - type: nauc_ndcg_at_1_max
      value: 40.8301
    - type: nauc_ndcg_at_1_std
      value: -4.7965
    - type: nauc_ndcg_at_1_diff1
      value: 47.0363
    - type: nauc_ndcg_at_3_max
      value: 38.1658
    - type: nauc_ndcg_at_3_std
      value: -5.5431
    - type: nauc_ndcg_at_3_diff1
      value: 43.236200000000004
    - type: nauc_ndcg_at_5_max
      value: 38.3776
    - type: nauc_ndcg_at_5_std
      value: -6.4315
    - type: nauc_ndcg_at_5_diff1
      value: 41.906
    - type: nauc_ndcg_at_10_max
      value: 38.246900000000004
    - type: nauc_ndcg_at_10_std
      value: -5.9109
    - type: nauc_ndcg_at_10_diff1
      value: 42.2073
    - type: nauc_ndcg_at_20_max
      value: 39.1442
    - type: nauc_ndcg_at_20_std
      value: -4.2145
    - type: nauc_ndcg_at_20_diff1
      value: 42.1173
    - type: nauc_ndcg_at_100_max
      value: 40.2409
    - type: nauc_ndcg_at_100_std
      value: -2.3533999999999997
    - type: nauc_ndcg_at_100_diff1
      value: 43.08
    - type: nauc_ndcg_at_1000_max
      value: 39.7135
    - type: nauc_ndcg_at_1000_std
      value: -3.2211999999999996
    - type: nauc_ndcg_at_1000_diff1
      value: 42.9532
    - type: nauc_map_at_1_max
      value: 34.8396
    - type: nauc_map_at_1_std
      value: -7.427200000000001
    - type: nauc_map_at_1_diff1
      value: 52.3057
    - type: nauc_map_at_3_max
      value: 36.869
    - type: nauc_map_at_3_std
      value: -7.482800000000001
    - type: nauc_map_at_3_diff1
      value: 46.7357
    - type: nauc_map_at_5_max
      value: 37.7915
    - type: nauc_map_at_5_std
      value: -7.4328
    - type: nauc_map_at_5_diff1
      value: 45.5111
    - type: nauc_map_at_10_max
      value: 38.1613
    - type: nauc_map_at_10_std
      value: -6.8068
    - type: nauc_map_at_10_diff1
      value: 45.359899999999996
    - type: nauc_map_at_20_max
      value: 38.5576
    - type: nauc_map_at_20_std
      value: -6.051200000000001
    - type: nauc_map_at_20_diff1
      value: 45.1212
    - type: nauc_map_at_100_max
      value: 38.8156
    - type: nauc_map_at_100_std
      value: -5.5418
    - type: nauc_map_at_100_diff1
      value: 45.1108
    - type: nauc_map_at_1000_max
      value: 38.746199999999995
    - type: nauc_map_at_1000_std
      value: -5.6205
    - type: nauc_map_at_1000_diff1
      value: 45.053399999999996
    - type: nauc_recall_at_1_max
      value: 34.8396
    - type: nauc_recall_at_1_std
      value: -7.427200000000001
    - type: nauc_recall_at_1_diff1
      value: 52.3057
    - type: nauc_recall_at_3_max
      value: 34.3365
    - type: nauc_recall_at_3_std
      value: -6.8784
    - type: nauc_recall_at_3_diff1
      value: 40.2233
    - type: nauc_recall_at_5_max
      value: 34.4245
    - type: nauc_recall_at_5_std
      value: -8.426300000000001
    - type: nauc_recall_at_5_diff1
      value: 35.4121
    - type: nauc_recall_at_10_max
      value: 32.2333
    - type: nauc_recall_at_10_std
      value: -5.8829
    - type: nauc_recall_at_10_diff1
      value: 34.0262
    - type: nauc_recall_at_20_max
      value: 36.256
    - type: nauc_recall_at_20_std
      value: 1.9085999999999999
    - type: nauc_recall_at_20_diff1
      value: 32.2877
    - type: nauc_recall_at_100_max
      value: 47.3573
    - type: nauc_recall_at_100_std
      value: 24.4303
    - type: nauc_recall_at_100_diff1
      value: 38.3181
    - type: nauc_recall_at_1000_max
      value: 63.5826
    - type: nauc_recall_at_1000_std
      value: 71.3349
    - type: nauc_recall_at_1000_diff1
      value: 40.771
    - type: nauc_precision_at_1_max
      value: 40.8301
    - type: nauc_precision_at_1_std
      value: -4.7965
    - type: nauc_precision_at_1_diff1
      value: 47.0363
    - type: nauc_precision_at_3_max
      value: 30.7605
    - type: nauc_precision_at_3_std
      value: -0.4
    - type: nauc_precision_at_3_diff1
      value: 17.099800000000002
    - type: nauc_precision_at_5_max
      value: 26.3274
    - type: nauc_precision_at_5_std
      value: 3.1927
    - type: nauc_precision_at_5_diff1
      value: 5.6719
    - type: nauc_precision_at_10_max
      value: 16.8618
    - type: nauc_precision_at_10_std
      value: 7.0584
    - type: nauc_precision_at_10_diff1
      value: -4.7258000000000004
    - type: nauc_precision_at_20_max
      value: 10.8993
    - type: nauc_precision_at_20_std
      value: 10.215499999999999
    - type: nauc_precision_at_20_diff1
      value: -10.8149
    - type: nauc_precision_at_100_max
      value: -0.0973
    - type: nauc_precision_at_100_std
      value: 9.3108
    - type: nauc_precision_at_100_diff1
      value: -19.0862
    - type: nauc_precision_at_1000_max
      value: -16.488
    - type: nauc_precision_at_1000_std
      value: -6.325
    - type: nauc_precision_at_1000_diff1
      value: -28.7621
    - type: nauc_mrr_at_1_max
      value: 40.8301
    - type: nauc_mrr_at_1_std
      value: -4.7965
    - type: nauc_mrr_at_1_diff1
      value: 47.0363
    - type: nauc_mrr_at_3_max
      value: 40.3492
    - type: nauc_mrr_at_3_std
      value: -4.0226
    - type: nauc_mrr_at_3_diff1
      value: 43.358799999999995
    - type: nauc_mrr_at_5_max
      value: 40.4342
    - type: nauc_mrr_at_5_std
      value: -4.5294
    - type: nauc_mrr_at_5_diff1
      value: 42.6362
    - type: nauc_mrr_at_10_max
      value: 40.2882
    - type: nauc_mrr_at_10_std
      value: -4.1685
    - type: nauc_mrr_at_10_diff1
      value: 42.5151
    - type: nauc_mrr_at_20_max
      value: 40.3939
    - type: nauc_mrr_at_20_std
      value: -4.1178
    - type: nauc_mrr_at_20_diff1
      value: 42.586400000000005
    - type: nauc_mrr_at_100_max
      value: 40.5002
    - type: nauc_mrr_at_100_std
      value: -4.0205
    - type: nauc_mrr_at_100_diff1
      value: 42.7299
    - type: nauc_mrr_at_1000_max
      value: 40.5002
    - type: nauc_mrr_at_1000_std
      value: -4.0168
    - type: nauc_mrr_at_1000_diff1
      value: 42.7356
    - type: main_score
      value: 57.667
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackEnglishRetrieval (default)
      revision: ad9991cb51e31e31e430383c75ffb2885547b5f0
      split: test
      type: mteb/cqadupstack-english
    metrics:
    - type: ndcg_at_1
      value: 45.478
    - type: ndcg_at_3
      value: 51.124
    - type: ndcg_at_5
      value: 53.166000000000004
    - type: ndcg_at_10
      value: 55.505
    - type: ndcg_at_20
      value: 57.154
    - type: ndcg_at_100
      value: 59.606
    - type: ndcg_at_1000
      value: 61.255
    - type: map_at_1
      value: 36.198
    - type: map_at_3
      value: 45.678000000000004
    - type: map_at_5
      value: 47.605
    - type: map_at_10
      value: 49.199
    - type: map_at_20
      value: 49.957
    - type: map_at_100
      value: 50.602000000000004
    - type: map_at_1000
      value: 50.736000000000004
    - type: recall_at_1
      value: 36.198
    - type: recall_at_3
      value: 53.20700000000001
    - type: recall_at_5
      value: 59.169000000000004
    - type: recall_at_10
      value: 66.465
    - type: recall_at_20
      value: 72.60799999999999
    - type: recall_at_100
      value: 83.63199999999999
    - type: recall_at_1000
      value: 93.27600000000001
    - type: precision_at_1
      value: 45.478
    - type: precision_at_3
      value: 25.052999999999997
    - type: precision_at_5
      value: 17.694
    - type: precision_at_10
      value: 10.752
    - type: precision_at_20
      value: 6.239
    - type: precision_at_100
      value: 1.6660000000000001
    - type: precision_at_1000
      value: 0.211
    - type: mrr_at_1
      value: 45.4777
    - type: mrr_at_3
      value: 52.887499999999996
    - type: mrr_at_5
      value: 54.282399999999996
    - type: mrr_at_10
      value: 55.0745
    - type: mrr_at_20
      value: 55.43090000000001
    - type: mrr_at_100
      value: 55.656000000000006
    - type: mrr_at_1000
      value: 55.688
    - type: nauc_ndcg_at_1_max
      value: 46.8217
    - type: nauc_ndcg_at_1_std
      value: -2.7794
    - type: nauc_ndcg_at_1_diff1
      value: 57.0574
    - type: nauc_ndcg_at_3_max
      value: 47.7532
    - type: nauc_ndcg_at_3_std
      value: -1.4668
    - type: nauc_ndcg_at_3_diff1
      value: 52.8335
    - type: nauc_ndcg_at_5_max
      value: 48.7828
    - type: nauc_ndcg_at_5_std
      value: -1.015
    - type: nauc_ndcg_at_5_diff1
      value: 51.991699999999994
    - type: nauc_ndcg_at_10_max
      value: 50.114999999999995
    - type: nauc_ndcg_at_10_std
      value: 1.1684
    - type: nauc_ndcg_at_10_diff1
      value: 51.9116
    - type: nauc_ndcg_at_20_max
      value: 50.006099999999996
    - type: nauc_ndcg_at_20_std
      value: 2.0345
    - type: nauc_ndcg_at_20_diff1
      value: 51.63870000000001
    - type: nauc_ndcg_at_100_max
      value: 50.478
    - type: nauc_ndcg_at_100_std
      value: 3.8077
    - type: nauc_ndcg_at_100_diff1
      value: 51.3939
    - type: nauc_ndcg_at_1000_max
      value: 50.0328
    - type: nauc_ndcg_at_1000_std
      value: 3.2628
    - type: nauc_ndcg_at_1000_diff1
      value: 51.5116
    - type: nauc_map_at_1_max
      value: 35.4528
    - type: nauc_map_at_1_std
      value: -12.8546
    - type: nauc_map_at_1_diff1
      value: 59.2294
    - type: nauc_map_at_3_max
      value: 42.8209
    - type: nauc_map_at_3_std
      value: -8.1284
    - type: nauc_map_at_3_diff1
      value: 55.5925
    - type: nauc_map_at_5_max
      value: 44.7278
    - type: nauc_map_at_5_std
      value: -6.311400000000001
    - type: nauc_map_at_5_diff1
      value: 54.6249
    - type: nauc_map_at_10_max
      value: 46.3085
    - type: nauc_map_at_10_std
      value: -4.2609
    - type: nauc_map_at_10_diff1
      value: 54.4523
    - type: nauc_map_at_20_max
      value: 46.8259
    - type: nauc_map_at_20_std
      value: -3.3686000000000003
    - type: nauc_map_at_20_diff1
      value: 54.225100000000005
    - type: nauc_map_at_100_max
      value: 47.4262
    - type: nauc_map_at_100_std
      value: -2.3889
    - type: nauc_map_at_100_diff1
      value: 54.01669999999999
    - type: nauc_map_at_1000_max
      value: 47.453
    - type: nauc_map_at_1000_std
      value: -2.3062
    - type: nauc_map_at_1000_diff1
      value: 53.9968
    - type: nauc_recall_at_1_max
      value: 35.4528
    - type: nauc_recall_at_1_std
      value: -12.8546
    - type: nauc_recall_at_1_diff1
      value: 59.2294
    - type: nauc_recall_at_3_max
      value: 42.7793
    - type: nauc_recall_at_3_std
      value: -4.7798
    - type: nauc_recall_at_3_diff1
      value: 49.741
    - type: nauc_recall_at_5_max
      value: 45.6544
    - type: nauc_recall_at_5_std
      value: -1.6133000000000002
    - type: nauc_recall_at_5_diff1
      value: 45.7699
    - type: nauc_recall_at_10_max
      value: 50.769
    - type: nauc_recall_at_10_std
      value: 7.4262
    - type: nauc_recall_at_10_diff1
      value: 43.3808
    - type: nauc_recall_at_20_max
      value: 51.0312
    - type: nauc_recall_at_20_std
      value: 12.7246
    - type: nauc_recall_at_20_diff1
      value: 40.5477
    - type: nauc_recall_at_100_max
      value: 56.3878
    - type: nauc_recall_at_100_std
      value: 31.893300000000004
    - type: nauc_recall_at_100_diff1
      value: 34.902699999999996
    - type: nauc_recall_at_1000_max
      value: 55.4185
    - type: nauc_recall_at_1000_std
      value: 48.0244
    - type: nauc_recall_at_1000_diff1
      value: 27.980300000000003
    - type: nauc_precision_at_1_max
      value: 46.8217
    - type: nauc_precision_at_1_std
      value: -2.7794
    - type: nauc_precision_at_1_diff1
      value: 57.0574
    - type: nauc_precision_at_3_max
      value: 45.9159
    - type: nauc_precision_at_3_std
      value: 14.8948
    - type: nauc_precision_at_3_diff1
      value: 25.3519
    - type: nauc_precision_at_5_max
      value: 44.908500000000004
    - type: nauc_precision_at_5_std
      value: 22.3321
    - type: nauc_precision_at_5_diff1
      value: 14.696600000000002
    - type: nauc_precision_at_10_max
      value: 40.1
    - type: nauc_precision_at_10_std
      value: 29.6731
    - type: nauc_precision_at_10_diff1
      value: 4.2817
    - type: nauc_precision_at_20_max
      value: 35.2526
    - type: nauc_precision_at_20_std
      value: 34.4698
    - type: nauc_precision_at_20_diff1
      value: -3.8809000000000005
    - type: nauc_precision_at_100_max
      value: 25.186500000000002
    - type: nauc_precision_at_100_std
      value: 38.684400000000004
    - type: nauc_precision_at_100_diff1
      value: -15.160599999999999
    - type: nauc_precision_at_1000_max
      value: 11.5275
    - type: nauc_precision_at_1000_std
      value: 29.2055
    - type: nauc_precision_at_1000_diff1
      value: -19.7629
    - type: nauc_mrr_at_1_max
      value: 46.8217
    - type: nauc_mrr_at_1_std
      value: -2.7794
    - type: nauc_mrr_at_1_diff1
      value: 57.0574
    - type: nauc_mrr_at_3_max
      value: 49.7145
    - type: nauc_mrr_at_3_std
      value: 0.7482
    - type: nauc_mrr_at_3_diff1
      value: 54.0562
    - type: nauc_mrr_at_5_max
      value: 50.0393
    - type: nauc_mrr_at_5_std
      value: 0.9629000000000001
    - type: nauc_mrr_at_5_diff1
      value: 53.41780000000001
    - type: nauc_mrr_at_10_max
      value: 50.325900000000004
    - type: nauc_mrr_at_10_std
      value: 1.6938000000000002
    - type: nauc_mrr_at_10_diff1
      value: 53.0736
    - type: nauc_mrr_at_20_max
      value: 50.1989
    - type: nauc_mrr_at_20_std
      value: 1.7967
    - type: nauc_mrr_at_20_diff1
      value: 52.9982
    - type: nauc_mrr_at_100_max
      value: 50.184799999999996
    - type: nauc_mrr_at_100_std
      value: 1.8381999999999998
    - type: nauc_mrr_at_100_diff1
      value: 53.034099999999995
    - type: nauc_mrr_at_1000_max
      value: 50.1706
    - type: nauc_mrr_at_1000_std
      value: 1.8124999999999998
    - type: nauc_mrr_at_1000_diff1
      value: 53.0505
    - type: main_score
      value: 55.505
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackGamingRetrieval (default)
      revision: 4885aa143210c98657558c04aaf3dc47cfb54340
      split: test
      type: mteb/cqadupstack-gaming
    metrics:
    - type: ndcg_at_1
      value: 50.09400000000001
    - type: ndcg_at_3
      value: 58.022
    - type: ndcg_at_5
      value: 60.97
    - type: ndcg_at_10
      value: 63.641000000000005
    - type: ndcg_at_20
      value: 65.273
    - type: ndcg_at_100
      value: 67.05499999999999
    - type: ndcg_at_1000
      value: 67.855
    - type: map_at_1
      value: 44.157000000000004
    - type: map_at_3
      value: 54.223
    - type: map_at_5
      value: 56.306999999999995
    - type: map_at_10
      value: 57.753
    - type: map_at_20
      value: 58.36900000000001
    - type: map_at_100
      value: 58.69799999999999
    - type: map_at_1000
      value: 58.74
    - type: recall_at_1
      value: 44.157000000000004
    - type: recall_at_3
      value: 63.087
    - type: recall_at_5
      value: 70.172
    - type: recall_at_10
      value: 77.78
    - type: recall_at_20
      value: 83.699
    - type: recall_at_100
      value: 92.244
    - type: recall_at_1000
      value: 97.81
    - type: precision_at_1
      value: 50.09400000000001
    - type: precision_at_3
      value: 25.81
    - type: precision_at_5
      value: 17.755000000000003
    - type: precision_at_10
      value: 10.181999999999999
    - type: precision_at_20
      value: 5.627
    - type: precision_at_100
      value: 1.278
    - type: precision_at_1000
      value: 0.13799999999999998
    - type: mrr_at_1
      value: 50.09400000000001
    - type: mrr_at_3
      value: 58.2654
    - type: mrr_at_5
      value: 59.8171
    - type: mrr_at_10
      value: 60.6998
    - type: mrr_at_20
      value: 61.077000000000005
    - type: mrr_at_100
      value: 61.2602
    - type: mrr_at_1000
      value: 61.2803
    - type: nauc_ndcg_at_1_max
      value: 42.0223
    - type: nauc_ndcg_at_1_std
      value: -7.5249999999999995
    - type: nauc_ndcg_at_1_diff1
      value: 57.545
    - type: nauc_ndcg_at_3_max
      value: 41.4981
    - type: nauc_ndcg_at_3_std
      value: -7.3598
    - type: nauc_ndcg_at_3_diff1
      value: 53.404399999999995
    - type: nauc_ndcg_at_5_max
      value: 43.1299
    - type: nauc_ndcg_at_5_std
      value: -5.4483999999999995
    - type: nauc_ndcg_at_5_diff1
      value: 52.86149999999999
    - type: nauc_ndcg_at_10_max
      value: 44.460899999999995
    - type: nauc_ndcg_at_10_std
      value: -3.5878
    - type: nauc_ndcg_at_10_diff1
      value: 53.24529999999999
    - type: nauc_ndcg_at_20_max
      value: 45.057199999999995
    - type: nauc_ndcg_at_20_std
      value: -2.5892999999999997
    - type: nauc_ndcg_at_20_diff1
      value: 53.14919999999999
    - type: nauc_ndcg_at_100_max
      value: 45.202
    - type: nauc_ndcg_at_100_std
      value: -1.6291
    - type: nauc_ndcg_at_100_diff1
      value: 53.226099999999995
    - type: nauc_ndcg_at_1000_max
      value: 44.9773
    - type: nauc_ndcg_at_1000_std
      value: -2.2944
    - type: nauc_ndcg_at_1000_diff1
      value: 53.5531
    - type: nauc_map_at_1_max
      value: 34.3597
    - type: nauc_map_at_1_std
      value: -8.7494
    - type: nauc_map_at_1_diff1
      value: 57.288399999999996
    - type: nauc_map_at_3_max
      value: 39.723000000000006
    - type: nauc_map_at_3_std
      value: -8.9697
    - type: nauc_map_at_3_diff1
      value: 55.0296
    - type: nauc_map_at_5_max
      value: 41.2509
    - type: nauc_map_at_5_std
      value: -7.561
    - type: nauc_map_at_5_diff1
      value: 54.641799999999996
    - type: nauc_map_at_10_max
      value: 42.2464
    - type: nauc_map_at_10_std
      value: -6.442699999999999
    - type: nauc_map_at_10_diff1
      value: 54.6922
    - type: nauc_map_at_20_max
      value: 42.6447
    - type: nauc_map_at_20_std
      value: -5.8575
    - type: nauc_map_at_20_diff1
      value: 54.607099999999996
    - type: nauc_map_at_100_max
      value: 42.801899999999996
    - type: nauc_map_at_100_std
      value: -5.5908
    - type: nauc_map_at_100_diff1
      value: 54.64
    - type: nauc_map_at_1000_max
      value: 42.8163
    - type: nauc_map_at_1000_std
      value: -5.5892
    - type: nauc_map_at_1000_diff1
      value: 54.657999999999994
    - type: nauc_recall_at_1_max
      value: 34.3597
    - type: nauc_recall_at_1_std
      value: -8.7494
    - type: nauc_recall_at_1_diff1
      value: 57.288399999999996
    - type: nauc_recall_at_3_max
      value: 38.2143
    - type: nauc_recall_at_3_std
      value: -8.5053
    - type: nauc_recall_at_3_diff1
      value: 48.5674
    - type: nauc_recall_at_5_max
      value: 42.4963
    - type: nauc_recall_at_5_std
      value: -3.1975000000000002
    - type: nauc_recall_at_5_diff1
      value: 46.1409
    - type: nauc_recall_at_10_max
      value: 47.5304
    - type: nauc_recall_at_10_std
      value: 4.2543
    - type: nauc_recall_at_10_diff1
      value: 46.187400000000004
    - type: nauc_recall_at_20_max
      value: 52.5031
    - type: nauc_recall_at_20_std
      value: 12.215
    - type: nauc_recall_at_20_diff1
      value: 43.959199999999996
    - type: nauc_recall_at_100_max
      value: 59.519800000000004
    - type: nauc_recall_at_100_std
      value: 36.355399999999996
    - type: nauc_recall_at_100_diff1
      value: 38.1615
    - type: nauc_recall_at_1000_max
      value: 75.7293
    - type: nauc_recall_at_1000_std
      value: 68.0791
    - type: nauc_recall_at_1000_diff1
      value: 33.4758
    - type: nauc_precision_at_1_max
      value: 42.0223
    - type: nauc_precision_at_1_std
      value: -7.5249999999999995
    - type: nauc_precision_at_1_diff1
      value: 57.545
    - type: nauc_precision_at_3_max
      value: 40.269800000000004
    - type: nauc_precision_at_3_std
      value: -0.1042
    - type: nauc_precision_at_3_diff1
      value: 28.7982
    - type: nauc_precision_at_5_max
      value: 37.8177
    - type: nauc_precision_at_5_std
      value: 6.5974
    - type: nauc_precision_at_5_diff1
      value: 17.729
    - type: nauc_precision_at_10_max
      value: 34.4199
    - type: nauc_precision_at_10_std
      value: 14.8032
    - type: nauc_precision_at_10_diff1
      value: 7.8933
    - type: nauc_precision_at_20_max
      value: 31.5289
    - type: nauc_precision_at_20_std
      value: 22.1412
    - type: nauc_precision_at_20_diff1
      value: -0.993
    - type: nauc_precision_at_100_max
      value: 24.3425
    - type: nauc_precision_at_100_std
      value: 27.3469
    - type: nauc_precision_at_100_diff1
      value: -9.3572
    - type: nauc_precision_at_1000_max
      value: 18.453500000000002
    - type: nauc_precision_at_1000_std
      value: 24.925800000000002
    - type: nauc_precision_at_1000_diff1
      value: -12.5892
    - type: nauc_mrr_at_1_max
      value: 42.0223
    - type: nauc_mrr_at_1_std
      value: -7.5249999999999995
    - type: nauc_mrr_at_1_diff1
      value: 57.545
    - type: nauc_mrr_at_3_max
      value: 43.4966
    - type: nauc_mrr_at_3_std
      value: -5.9497
    - type: nauc_mrr_at_3_diff1
      value: 54.3814
    - type: nauc_mrr_at_5_max
      value: 43.918
    - type: nauc_mrr_at_5_std
      value: -5.048
    - type: nauc_mrr_at_5_diff1
      value: 53.9473
    - type: nauc_mrr_at_10_max
      value: 43.9711
    - type: nauc_mrr_at_10_std
      value: -4.6621999999999995
    - type: nauc_mrr_at_10_diff1
      value: 54.231399999999994
    - type: nauc_mrr_at_20_max
      value: 44.0448
    - type: nauc_mrr_at_20_std
      value: -4.564900000000001
    - type: nauc_mrr_at_20_diff1
      value: 54.2486
    - type: nauc_mrr_at_100_max
      value: 44.0305
    - type: nauc_mrr_at_100_std
      value: -4.5347
    - type: nauc_mrr_at_100_diff1
      value: 54.2802
    - type: nauc_mrr_at_1000_max
      value: 44.0239
    - type: nauc_mrr_at_1000_std
      value: -4.5523
    - type: nauc_mrr_at_1000_diff1
      value: 54.2908
    - type: main_score
      value: 63.641000000000005
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackGisRetrieval (default)
      revision: 5003b3064772da1887988e05400cf3806fe491f2
      split: test
      type: mteb/cqadupstack-gis
    metrics:
    - type: ndcg_at_1
      value: 32.09
    - type: ndcg_at_3
      value: 40.149
    - type: ndcg_at_5
      value: 43.111
    - type: ndcg_at_10
      value: 46.075
    - type: ndcg_at_20
      value: 48.17
    - type: ndcg_at_100
      value: 51.03
    - type: ndcg_at_1000
      value: 52.668000000000006
    - type: map_at_1
      value: 29.532000000000004
    - type: map_at_3
      value: 37.086000000000006
    - type: map_at_5
      value: 38.889
    - type: map_at_10
      value: 40.214
    - type: map_at_20
      value: 40.831
    - type: map_at_100
      value: 41.289
    - type: map_at_1000
      value: 41.359
    - type: recall_at_1
      value: 29.532000000000004
    - type: recall_at_3
      value: 46.03
    - type: recall_at_5
      value: 53.089
    - type: recall_at_10
      value: 62.025
    - type: recall_at_20
      value: 69.762
    - type: recall_at_100
      value: 83.829
    - type: recall_at_1000
      value: 95.99499999999999
    - type: precision_at_1
      value: 32.09
    - type: precision_at_3
      value: 17.175
    - type: precision_at_5
      value: 12.068
    - type: precision_at_10
      value: 7.141
    - type: precision_at_20
      value: 4.079
    - type: precision_at_100
      value: 1.018
    - type: precision_at_1000
      value: 0.11800000000000001
    - type: mrr_at_1
      value: 32.0904
    - type: mrr_at_3
      value: 39.7363
    - type: mrr_at_5
      value: 41.307
    - type: mrr_at_10
      value: 42.4232
    - type: mrr_at_20
      value: 42.9925
    - type: mrr_at_100
      value: 43.342000000000006
    - type: mrr_at_1000
      value: 43.3947
    - type: nauc_ndcg_at_1_max
      value: 28.6057
    - type: nauc_ndcg_at_1_std
      value: -9.5015
    - type: nauc_ndcg_at_1_diff1
      value: 45.895599999999995
    - type: nauc_ndcg_at_3_max
      value: 27.4486
    - type: nauc_ndcg_at_3_std
      value: -8.3694
    - type: nauc_ndcg_at_3_diff1
      value: 40.1689
    - type: nauc_ndcg_at_5_max
      value: 29.481299999999997
    - type: nauc_ndcg_at_5_std
      value: -5.382
    - type: nauc_ndcg_at_5_diff1
      value: 39.5505
    - type: nauc_ndcg_at_10_max
      value: 29.629299999999997
    - type: nauc_ndcg_at_10_std
      value: -3.1249
    - type: nauc_ndcg_at_10_diff1
      value: 37.953199999999995
    - type: nauc_ndcg_at_20_max
      value: 29.5532
    - type: nauc_ndcg_at_20_std
      value: -2.7831
    - type: nauc_ndcg_at_20_diff1
      value: 37.2522
    - type: nauc_ndcg_at_100_max
      value: 29.741600000000002
    - type: nauc_ndcg_at_100_std
      value: -3.2703999999999995
    - type: nauc_ndcg_at_100_diff1
      value: 37.7396
    - type: nauc_ndcg_at_1000_max
      value: 29.9018
    - type: nauc_ndcg_at_1000_std
      value: -3.6946
    - type: nauc_ndcg_at_1000_diff1
      value: 38.5323
    - type: nauc_map_at_1_max
      value: 25.423299999999998
    - type: nauc_map_at_1_std
      value: -12.3377
    - type: nauc_map_at_1_diff1
      value: 46.8633
    - type: nauc_map_at_3_max
      value: 26.4335
    - type: nauc_map_at_3_std
      value: -9.871
    - type: nauc_map_at_3_diff1
      value: 41.9019
    - type: nauc_map_at_5_max
      value: 27.852
    - type: nauc_map_at_5_std
      value: -8.0967
    - type: nauc_map_at_5_diff1
      value: 41.4142
    - type: nauc_map_at_10_max
      value: 28.163700000000002
    - type: nauc_map_at_10_std
      value: -6.9023
    - type: nauc_map_at_10_diff1
      value: 40.779399999999995
    - type: nauc_map_at_20_max
      value: 28.1646
    - type: nauc_map_at_20_std
      value: -6.7966999999999995
    - type: nauc_map_at_20_diff1
      value: 40.625299999999996
    - type: nauc_map_at_100_max
      value: 28.2439
    - type: nauc_map_at_100_std
      value: -6.7998
    - type: nauc_map_at_100_diff1
      value: 40.7153
    - type: nauc_map_at_1000_max
      value: 28.2633
    - type: nauc_map_at_1000_std
      value: -6.802
    - type: nauc_map_at_1000_diff1
      value: 40.748
    - type: nauc_recall_at_1_max
      value: 25.423299999999998
    - type: nauc_recall_at_1_std
      value: -12.3377
    - type: nauc_recall_at_1_diff1
      value: 46.8633
    - type: nauc_recall_at_3_max
      value: 26.378800000000002
    - type: nauc_recall_at_3_std
      value: -6.6701
    - type: nauc_recall_at_3_diff1
      value: 35.8097
    - type: nauc_recall_at_5_max
      value: 30.9445
    - type: nauc_recall_at_5_std
      value: 0.1917
    - type: nauc_recall_at_5_diff1
      value: 33.5229
    - type: nauc_recall_at_10_max
      value: 30.995099999999997
    - type: nauc_recall_at_10_std
      value: 7.613200000000001
    - type: nauc_recall_at_10_diff1
      value: 27.2905
    - type: nauc_recall_at_20_max
      value: 31.244
    - type: nauc_recall_at_20_std
      value: 11.0527
    - type: nauc_recall_at_20_diff1
      value: 22.5701
    - type: nauc_recall_at_100_max
      value: 33.293
    - type: nauc_recall_at_100_std
      value: 12.4908
    - type: nauc_recall_at_100_diff1
      value: 19.2291
    - type: nauc_recall_at_1000_max
      value: 52.0915
    - type: nauc_recall_at_1000_std
      value: 32.1464
    - type: nauc_recall_at_1000_diff1
      value: 14.0362
    - type: nauc_precision_at_1_max
      value: 28.6057
    - type: nauc_precision_at_1_std
      value: -9.5015
    - type: nauc_precision_at_1_diff1
      value: 45.895599999999995
    - type: nauc_precision_at_3_max
      value: 31.391599999999997
    - type: nauc_precision_at_3_std
      value: -2.6111
    - type: nauc_precision_at_3_diff1
      value: 31.983800000000002
    - type: nauc_precision_at_5_max
      value: 35.9814
    - type: nauc_precision_at_5_std
      value: 6.062
    - type: nauc_precision_at_5_diff1
      value: 27.8588
    - type: nauc_precision_at_10_max
      value: 34.5678
    - type: nauc_precision_at_10_std
      value: 14.2625
    - type: nauc_precision_at_10_diff1
      value: 19.7208
    - type: nauc_precision_at_20_max
      value: 31.451600000000003
    - type: nauc_precision_at_20_std
      value: 16.6162
    - type: nauc_precision_at_20_diff1
      value: 12.421100000000001
    - type: nauc_precision_at_100_max
      value: 22.1049
    - type: nauc_precision_at_100_std
      value: 16.4354
    - type: nauc_precision_at_100_diff1
      value: 0.5193
    - type: nauc_precision_at_1000_max
      value: 14.682899999999998
    - type: nauc_precision_at_1000_std
      value: 15.5581
    - type: nauc_precision_at_1000_diff1
      value: -9.7103
    - type: nauc_mrr_at_1_max
      value: 28.6057
    - type: nauc_mrr_at_1_std
      value: -9.5015
    - type: nauc_mrr_at_1_diff1
      value: 45.895599999999995
    - type: nauc_mrr_at_3_max
      value: 29.082400000000003
    - type: nauc_mrr_at_3_std
      value: -6.9314
    - type: nauc_mrr_at_3_diff1
      value: 40.9506
    - type: nauc_mrr_at_5_max
      value: 30.152600000000003
    - type: nauc_mrr_at_5_std
      value: -5.455900000000001
    - type: nauc_mrr_at_5_diff1
      value: 40.7747
    - type: nauc_mrr_at_10_max
      value: 29.9987
    - type: nauc_mrr_at_10_std
      value: -4.839799999999999
    - type: nauc_mrr_at_10_diff1
      value: 40.2137
    - type: nauc_mrr_at_20_max
      value: 29.842200000000002
    - type: nauc_mrr_at_20_std
      value: -4.864
    - type: nauc_mrr_at_20_diff1
      value: 39.970800000000004
    - type: nauc_mrr_at_100_max
      value: 29.8359
    - type: nauc_mrr_at_100_std
      value: -4.9491
    - type: nauc_mrr_at_100_diff1
      value: 40.0495
    - type: nauc_mrr_at_1000_max
      value: 29.837799999999998
    - type: nauc_mrr_at_1000_std
      value: -4.968
    - type: nauc_mrr_at_1000_diff1
      value: 40.0797
    - type: main_score
      value: 46.075
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackMathematicaRetrieval (default)
      revision: 90fceea13679c63fe563ded68f3b6f06e50061de
      split: test
      type: mteb/cqadupstack-mathematica
    metrics:
    - type: ndcg_at_1
      value: 23.756
    - type: ndcg_at_3
      value: 29.725
    - type: ndcg_at_5
      value: 32.879000000000005
    - type: ndcg_at_10
      value: 36.015
    - type: ndcg_at_20
      value: 38.753
    - type: ndcg_at_100
      value: 42.175000000000004
    - type: ndcg_at_1000
      value: 44.607
    - type: map_at_1
      value: 18.944
    - type: map_at_3
      value: 26.098
    - type: map_at_5
      value: 28.151
    - type: map_at_10
      value: 29.610999999999997
    - type: map_at_20
      value: 30.481
    - type: map_at_100
      value: 31.063000000000002
    - type: map_at_1000
      value: 31.174000000000003
    - type: recall_at_1
      value: 18.944
    - type: recall_at_3
      value: 33.611000000000004
    - type: recall_at_5
      value: 41.427
    - type: recall_at_10
      value: 50.690999999999995
    - type: recall_at_20
      value: 60.437
    - type: recall_at_100
      value: 76.503
    - type: recall_at_1000
      value: 93.624
    - type: precision_at_1
      value: 23.756
    - type: precision_at_3
      value: 14.635000000000002
    - type: precision_at_5
      value: 11.07
    - type: precision_at_10
      value: 6.927999999999999
    - type: precision_at_20
      value: 4.266
    - type: precision_at_100
      value: 1.153
    - type: precision_at_1000
      value: 0.149
    - type: mrr_at_1
      value: 23.7562
    - type: mrr_at_3
      value: 31.2604
    - type: mrr_at_5
      value: 33.1696
    - type: mrr_at_10
      value: 34.4913
    - type: mrr_at_20
      value: 35.111399999999996
    - type: mrr_at_100
      value: 35.457499999999996
    - type: mrr_at_1000
      value: 35.5125
    - type: nauc_ndcg_at_1_max
      value: 16.369
    - type: nauc_ndcg_at_1_std
      value: -0.2643
    - type: nauc_ndcg_at_1_diff1
      value: 36.3924
    - type: nauc_ndcg_at_3_max
      value: 16.8313
    - type: nauc_ndcg_at_3_std
      value: -2.5591
    - type: nauc_ndcg_at_3_diff1
      value: 31.2622
    - type: nauc_ndcg_at_5_max
      value: 16.575899999999997
    - type: nauc_ndcg_at_5_std
      value: -1.2212
    - type: nauc_ndcg_at_5_diff1
      value: 30.4259
    - type: nauc_ndcg_at_10_max
      value: 16.7024
    - type: nauc_ndcg_at_10_std
      value: -0.5341
    - type: nauc_ndcg_at_10_diff1
      value: 30.1232
    - type: nauc_ndcg_at_20_max
      value: 16.5942
    - type: nauc_ndcg_at_20_std
      value: -0.3493
    - type: nauc_ndcg_at_20_diff1
      value: 29.1065
    - type: nauc_ndcg_at_100_max
      value: 17.6591
    - type: nauc_ndcg_at_100_std
      value: 1.9944
    - type: nauc_ndcg_at_100_diff1
      value: 29.332399999999996
    - type: nauc_ndcg_at_1000_max
      value: 17.7443
    - type: nauc_ndcg_at_1000_std
      value: 1.6357
    - type: nauc_ndcg_at_1000_diff1
      value: 30.1231
    - type: nauc_map_at_1_max
      value: 13.264400000000002
    - type: nauc_map_at_1_std
      value: -2.1641
    - type: nauc_map_at_1_diff1
      value: 37.446200000000005
    - type: nauc_map_at_3_max
      value: 14.9032
    - type: nauc_map_at_3_std
      value: -2.714
    - type: nauc_map_at_3_diff1
      value: 32.5923
    - type: nauc_map_at_5_max
      value: 14.932500000000001
    - type: nauc_map_at_5_std
      value: -1.9889000000000001
    - type: nauc_map_at_5_diff1
      value: 31.879600000000003
    - type: nauc_map_at_10_max
      value: 15.309500000000002
    - type: nauc_map_at_10_std
      value: -1.5512
    - type: nauc_map_at_10_diff1
      value: 31.694899999999997
    - type: nauc_map_at_20_max
      value: 15.3357
    - type: nauc_map_at_20_std
      value: -1.4588999999999999
    - type: nauc_map_at_20_diff1
      value: 31.323800000000002
    - type: nauc_map_at_100_max
      value: 15.598
    - type: nauc_map_at_100_std
      value: -0.9811000000000001
    - type: nauc_map_at_100_diff1
      value: 31.434600000000003
    - type: nauc_map_at_1000_max
      value: 15.6096
    - type: nauc_map_at_1000_std
      value: -0.9884999999999999
    - type: nauc_map_at_1000_diff1
      value: 31.4697
    - type: nauc_recall_at_1_max
      value: 13.264400000000002
    - type: nauc_recall_at_1_std
      value: -2.1641
    - type: nauc_recall_at_1_diff1
      value: 37.446200000000005
    - type: nauc_recall_at_3_max
      value: 15.945500000000001
    - type: nauc_recall_at_3_std
      value: -3.4730999999999996
    - type: nauc_recall_at_3_diff1
      value: 27.0913
    - type: nauc_recall_at_5_max
      value: 15.237800000000002
    - type: nauc_recall_at_5_std
      value: -1.0399
    - type: nauc_recall_at_5_diff1
      value: 25.2793
    - type: nauc_recall_at_10_max
      value: 15.1746
    - type: nauc_recall_at_10_std
      value: 0.5708000000000001
    - type: nauc_recall_at_10_diff1
      value: 24.2515
    - type: nauc_recall_at_20_max
      value: 14.3294
    - type: nauc_recall_at_20_std
      value: 0.8943
    - type: nauc_recall_at_20_diff1
      value: 20.1567
    - type: nauc_recall_at_100_max
      value: 19.405
    - type: nauc_recall_at_100_std
      value: 15.5971
    - type: nauc_recall_at_100_diff1
      value: 16.8
    - type: nauc_recall_at_1000_max
      value: 27.3117
    - type: nauc_recall_at_1000_std
      value: 36.0277
    - type: nauc_recall_at_1000_diff1
      value: 15.1497
    - type: nauc_precision_at_1_max
      value: 16.369
    - type: nauc_precision_at_1_std
      value: -0.2643
    - type: nauc_precision_at_1_diff1
      value: 36.3924
    - type: nauc_precision_at_3_max
      value: 19.78
    - type: nauc_precision_at_3_std
      value: -2.0522
    - type: nauc_precision_at_3_diff1
      value: 24.3712
    - type: nauc_precision_at_5_max
      value: 19.4882
    - type: nauc_precision_at_5_std
      value: 0.7147
    - type: nauc_precision_at_5_diff1
      value: 20.2841
    - type: nauc_precision_at_10_max
      value: 20.0931
    - type: nauc_precision_at_10_std
      value: 3.0831
    - type: nauc_precision_at_10_diff1
      value: 15.928899999999999
    - type: nauc_precision_at_20_max
      value: 17.5823
    - type: nauc_precision_at_20_std
      value: 4.1056
    - type: nauc_precision_at_20_diff1
      value: 9.211500000000001
    - type: nauc_precision_at_100_max
      value: 14.447399999999998
    - type: nauc_precision_at_100_std
      value: 10.1543
    - type: nauc_precision_at_100_diff1
      value: 3.5811999999999995
    - type: nauc_precision_at_1000_max
      value: 7.829899999999999
    - type: nauc_precision_at_1000_std
      value: 3.4869999999999997
    - type: nauc_precision_at_1000_diff1
      value: -0.5313
    - type: nauc_mrr_at_1_max
      value: 16.369
    - type: nauc_mrr_at_1_std
      value: -0.2643
    - type: nauc_mrr_at_1_diff1
      value: 36.3924
    - type: nauc_mrr_at_3_max
      value: 18.8798
    - type: nauc_mrr_at_3_std
      value: -0.7811
    - type: nauc_mrr_at_3_diff1
      value: 31.7255
    - type: nauc_mrr_at_5_max
      value: 18.840799999999998
    - type: nauc_mrr_at_5_std
      value: -0.0676
    - type: nauc_mrr_at_5_diff1
      value: 31.6753
    - type: nauc_mrr_at_10_max
      value: 18.8049
    - type: nauc_mrr_at_10_std
      value: 0.2359
    - type: nauc_mrr_at_10_diff1
      value: 31.729200000000002
    - type: nauc_mrr_at_20_max
      value: 18.709999999999997
    - type: nauc_mrr_at_20_std
      value: 0.2533
    - type: nauc_mrr_at_20_diff1
      value: 31.556099999999997
    - type: nauc_mrr_at_100_max
      value: 18.7625
    - type: nauc_mrr_at_100_std
      value: 0.411
    - type: nauc_mrr_at_100_diff1
      value: 31.575599999999998
    - type: nauc_mrr_at_1000_max
      value: 18.7525
    - type: nauc_mrr_at_1000_std
      value: 0.4194
    - type: nauc_mrr_at_1000_diff1
      value: 31.6052
    - type: main_score
      value: 36.015
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackPhysicsRetrieval (default)
      revision: 79531abbd1fb92d06c6d6315a0cbbbf5bb247ea4
      split: test
      type: mteb/cqadupstack-physics
    metrics:
    - type: ndcg_at_1
      value: 42.348
    - type: ndcg_at_3
      value: 48.478
    - type: ndcg_at_5
      value: 50.79
    - type: ndcg_at_10
      value: 53.504
    - type: ndcg_at_20
      value: 55.753
    - type: ndcg_at_100
      value: 58.899
    - type: ndcg_at_1000
      value: 60.32300000000001
    - type: map_at_1
      value: 33.824
    - type: map_at_3
      value: 43.335
    - type: map_at_5
      value: 45.279
    - type: map_at_10
      value: 46.867999999999995
    - type: map_at_20
      value: 47.714
    - type: map_at_100
      value: 48.306
    - type: map_at_1000
      value: 48.406
    - type: recall_at_1
      value: 33.824
    - type: recall_at_3
      value: 52.305
    - type: recall_at_5
      value: 58.804
    - type: recall_at_10
      value: 67.142
    - type: recall_at_20
      value: 74.694
    - type: recall_at_100
      value: 89.134
    - type: recall_at_1000
      value: 97.816
    - type: precision_at_1
      value: 42.348
    - type: precision_at_3
      value: 23.741
    - type: precision_at_5
      value: 16.439
    - type: precision_at_10
      value: 9.75
    - type: precision_at_20
      value: 5.702999999999999
    - type: precision_at_100
      value: 1.466
    - type: precision_at_1000
      value: 0.17700000000000002
    - type: mrr_at_1
      value: 42.348400000000005
    - type: mrr_at_3
      value: 50.721799999999995
    - type: mrr_at_5
      value: 52.0115
    - type: mrr_at_10
      value: 52.9721
    - type: mrr_at_20
      value: 53.3914
    - type: mrr_at_100
      value: 53.7068
    - type: mrr_at_1000
      value: 53.734300000000005
    - type: nauc_ndcg_at_1_max
      value: 36.8685
    - type: nauc_ndcg_at_1_std
      value: -1.9057000000000002
    - type: nauc_ndcg_at_1_diff1
      value: 54.151700000000005
    - type: nauc_ndcg_at_3_max
      value: 36.8356
    - type: nauc_ndcg_at_3_std
      value: -3.5336
    - type: nauc_ndcg_at_3_diff1
      value: 48.3439
    - type: nauc_ndcg_at_5_max
      value: 35.705999999999996
    - type: nauc_ndcg_at_5_std
      value: -4.5076
    - type: nauc_ndcg_at_5_diff1
      value: 47.5611
    - type: nauc_ndcg_at_10_max
      value: 36.7768
    - type: nauc_ndcg_at_10_std
      value: -2.459
    - type: nauc_ndcg_at_10_diff1
      value: 47.254400000000004
    - type: nauc_ndcg_at_20_max
      value: 37.390499999999996
    - type: nauc_ndcg_at_20_std
      value: -2.2398000000000002
    - type: nauc_ndcg_at_20_diff1
      value: 47.8108
    - type: nauc_ndcg_at_100_max
      value: 38.3272
    - type: nauc_ndcg_at_100_std
      value: -0.3307
    - type: nauc_ndcg_at_100_diff1
      value: 48.4739
    - type: nauc_ndcg_at_1000_max
      value: 38.0766
    - type: nauc_ndcg_at_1000_std
      value: -0.6526
    - type: nauc_ndcg_at_1000_diff1
      value: 48.6232
    - type: nauc_map_at_1_max
      value: 29.901600000000002
    - type: nauc_map_at_1_std
      value: -7.186299999999999
    - type: nauc_map_at_1_diff1
      value: 54.2246
    - type: nauc_map_at_3_max
      value: 34.083200000000005
    - type: nauc_map_at_3_std
      value: -5.532
    - type: nauc_map_at_3_diff1
      value: 49.6089
    - type: nauc_map_at_5_max
      value: 34.2724
    - type: nauc_map_at_5_std
      value: -5.4413
    - type: nauc_map_at_5_diff1
      value: 49.045
    - type: nauc_map_at_10_max
      value: 35.3456
    - type: nauc_map_at_10_std
      value: -4.0495
    - type: nauc_map_at_10_diff1
      value: 48.9439
    - type: nauc_map_at_20_max
      value: 35.7489
    - type: nauc_map_at_20_std
      value: -3.769
    - type: nauc_map_at_20_diff1
      value: 49.205799999999996
    - type: nauc_map_at_100_max
      value: 35.9745
    - type: nauc_map_at_100_std
      value: -3.4292000000000002
    - type: nauc_map_at_100_diff1
      value: 49.2921
    - type: nauc_map_at_1000_max
      value: 35.9764
    - type: nauc_map_at_1000_std
      value: -3.4297
    - type: nauc_map_at_1000_diff1
      value: 49.3113
    - type: nauc_recall_at_1_max
      value: 29.901600000000002
    - type: nauc_recall_at_1_std
      value: -7.186299999999999
    - type: nauc_recall_at_1_diff1
      value: 54.2246
    - type: nauc_recall_at_3_max
      value: 32.3363
    - type: nauc_recall_at_3_std
      value: -6.5791
    - type: nauc_recall_at_3_diff1
      value: 41.86
    - type: nauc_recall_at_5_max
      value: 30.5954
    - type: nauc_recall_at_5_std
      value: -7.989599999999999
    - type: nauc_recall_at_5_diff1
      value: 38.5503
    - type: nauc_recall_at_10_max
      value: 34.238800000000005
    - type: nauc_recall_at_10_std
      value: -0.756
    - type: nauc_recall_at_10_diff1
      value: 36.8704
    - type: nauc_recall_at_20_max
      value: 35.7313
    - type: nauc_recall_at_20_std
      value: -0.7048
    - type: nauc_recall_at_20_diff1
      value: 37.7093
    - type: nauc_recall_at_100_max
      value: 44.4053
    - type: nauc_recall_at_100_std
      value: 20.2029
    - type: nauc_recall_at_100_diff1
      value: 38.6378
    - type: nauc_recall_at_1000_max
      value: 49.026399999999995
    - type: nauc_recall_at_1000_std
      value: 52.3613
    - type: nauc_recall_at_1000_diff1
      value: 27.487299999999998
    - type: nauc_precision_at_1_max
      value: 36.8685
    - type: nauc_precision_at_1_std
      value: -1.9057000000000002
    - type: nauc_precision_at_1_diff1
      value: 54.151700000000005
    - type: nauc_precision_at_3_max
      value: 36.608000000000004
    - type: nauc_precision_at_3_std
      value: 6.3276
    - type: nauc_precision_at_3_diff1
      value: 28.842499999999998
    - type: nauc_precision_at_5_max
      value: 32.2883
    - type: nauc_precision_at_5_std
      value: 8.0263
    - type: nauc_precision_at_5_diff1
      value: 21.2274
    - type: nauc_precision_at_10_max
      value: 30.814700000000002
    - type: nauc_precision_at_10_std
      value: 15.4999
    - type: nauc_precision_at_10_diff1
      value: 12.3553
    - type: nauc_precision_at_20_max
      value: 25.9789
    - type: nauc_precision_at_20_std
      value: 17.128
    - type: nauc_precision_at_20_diff1
      value: 7.342
    - type: nauc_precision_at_100_max
      value: 15.9879
    - type: nauc_precision_at_100_std
      value: 21.1499
    - type: nauc_precision_at_100_diff1
      value: -3.0609
    - type: nauc_precision_at_1000_max
      value: 4.850899999999999
    - type: nauc_precision_at_1000_std
      value: 15.750800000000002
    - type: nauc_precision_at_1000_diff1
      value: -9.2357
    - type: nauc_mrr_at_1_max
      value: 36.8685
    - type: nauc_mrr_at_1_std
      value: -1.9057000000000002
    - type: nauc_mrr_at_1_diff1
      value: 54.151700000000005
    - type: nauc_mrr_at_3_max
      value: 38.8422
    - type: nauc_mrr_at_3_std
      value: -1.3892
    - type: nauc_mrr_at_3_diff1
      value: 50.258100000000006
    - type: nauc_mrr_at_5_max
      value: 38.404500000000006
    - type: nauc_mrr_at_5_std
      value: -1.7023
    - type: nauc_mrr_at_5_diff1
      value: 49.7593
    - type: nauc_mrr_at_10_max
      value: 38.8727
    - type: nauc_mrr_at_10_std
      value: -1.0441
    - type: nauc_mrr_at_10_diff1
      value: 49.9366
    - type: nauc_mrr_at_20_max
      value: 38.8639
    - type: nauc_mrr_at_20_std
      value: -1.1834
    - type: nauc_mrr_at_20_diff1
      value: 50.004400000000004
    - type: nauc_mrr_at_100_max
      value: 38.8551
    - type: nauc_mrr_at_100_std
      value: -1.098
    - type: nauc_mrr_at_100_diff1
      value: 50.0522
    - type: nauc_mrr_at_1000_max
      value: 38.844699999999996
    - type: nauc_mrr_at_1000_std
      value: -1.117
    - type: nauc_mrr_at_1000_diff1
      value: 50.055099999999996
    - type: main_score
      value: 53.504
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackProgrammersRetrieval (default)
      revision: 6184bc1440d2dbc7612be22b50686b8826d22b32
      split: test
      type: mteb/cqadupstack-programmers
    metrics:
    - type: ndcg_at_1
      value: 37.557
    - type: ndcg_at_3
      value: 42.573
    - type: ndcg_at_5
      value: 45.528
    - type: ndcg_at_10
      value: 48.742999999999995
    - type: ndcg_at_20
      value: 51.160000000000004
    - type: ndcg_at_100
      value: 54.458
    - type: ndcg_at_1000
      value: 56.076
    - type: map_at_1
      value: 30.125
    - type: map_at_3
      value: 38.018
    - type: map_at_5
      value: 40.367999999999995
    - type: map_at_10
      value: 42.119
    - type: map_at_20
      value: 42.970000000000006
    - type: map_at_100
      value: 43.599
    - type: map_at_1000
      value: 43.69
    - type: recall_at_1
      value: 30.125
    - type: recall_at_3
      value: 45.437
    - type: recall_at_5
      value: 53.197
    - type: recall_at_10
      value: 62.619
    - type: recall_at_20
      value: 71.187
    - type: recall_at_100
      value: 86.574
    - type: recall_at_1000
      value: 97.102
    - type: precision_at_1
      value: 37.557
    - type: precision_at_3
      value: 20.624000000000002
    - type: precision_at_5
      value: 15.068000000000001
    - type: precision_at_10
      value: 9.269
    - type: precision_at_20
      value: 5.428
    - type: precision_at_100
      value: 1.401
    - type: precision_at_1000
      value: 0.16999999999999998
    - type: mrr_at_1
      value: 37.5571
    - type: mrr_at_3
      value: 44.6537
    - type: mrr_at_5
      value: 46.4403
    - type: mrr_at_10
      value: 47.5732
    - type: mrr_at_20
      value: 48.126000000000005
    - type: mrr_at_100
      value: 48.460300000000004
    - type: mrr_at_1000
      value: 48.4993
    - type: nauc_ndcg_at_1_max
      value: 44.5645
    - type: nauc_ndcg_at_1_std
      value: 4.542800000000001
    - type: nauc_ndcg_at_1_diff1
      value: 50.2359
    - type: nauc_ndcg_at_3_max
      value: 43.0652
    - type: nauc_ndcg_at_3_std
      value: 4.3627
    - type: nauc_ndcg_at_3_diff1
      value: 43.4871
    - type: nauc_ndcg_at_5_max
      value: 43.419999999999995
    - type: nauc_ndcg_at_5_std
      value: 6.1539
    - type: nauc_ndcg_at_5_diff1
      value: 43.6875
    - type: nauc_ndcg_at_10_max
      value: 43.5052
    - type: nauc_ndcg_at_10_std
      value: 8.0707
    - type: nauc_ndcg_at_10_diff1
      value: 43.7523
    - type: nauc_ndcg_at_20_max
      value: 44.0535
    - type: nauc_ndcg_at_20_std
      value: 8.9662
    - type: nauc_ndcg_at_20_diff1
      value: 42.869299999999996
    - type: nauc_ndcg_at_100_max
      value: 45.4324
    - type: nauc_ndcg_at_100_std
      value: 10.663400000000001
    - type: nauc_ndcg_at_100_diff1
      value: 44.3052
    - type: nauc_ndcg_at_1000_max
      value: 44.9238
    - type: nauc_ndcg_at_1000_std
      value: 9.0618
    - type: nauc_ndcg_at_1000_diff1
      value: 44.472699999999996
    - type: nauc_map_at_1_max
      value: 37.0128
    - type: nauc_map_at_1_std
      value: -1.8889
    - type: nauc_map_at_1_diff1
      value: 50.125299999999996
    - type: nauc_map_at_3_max
      value: 40.4277
    - type: nauc_map_at_3_std
      value: 1.5571
    - type: nauc_map_at_3_diff1
      value: 45.5239
    - type: nauc_map_at_5_max
      value: 41.6298
    - type: nauc_map_at_5_std
      value: 3.4013
    - type: nauc_map_at_5_diff1
      value: 45.3778
    - type: nauc_map_at_10_max
      value: 42.289300000000004
    - type: nauc_map_at_10_std
      value: 4.6503000000000005
    - type: nauc_map_at_10_diff1
      value: 45.5387
    - type: nauc_map_at_20_max
      value: 42.642
    - type: nauc_map_at_20_std
      value: 5.0203
    - type: nauc_map_at_20_diff1
      value: 45.1577
    - type: nauc_map_at_100_max
      value: 42.965199999999996
    - type: nauc_map_at_100_std
      value: 5.335
    - type: nauc_map_at_100_diff1
      value: 45.406800000000004
    - type: nauc_map_at_1000_max
      value: 42.9348
    - type: nauc_map_at_1000_std
      value: 5.2551
    - type: nauc_map_at_1000_diff1
      value: 45.408100000000005
    - type: nauc_recall_at_1_max
      value: 37.0128
    - type: nauc_recall_at_1_std
      value: -1.8889
    - type: nauc_recall_at_1_diff1
      value: 50.125299999999996
    - type: nauc_recall_at_3_max
      value: 38.929
    - type: nauc_recall_at_3_std
      value: 4.077
    - type: nauc_recall_at_3_diff1
      value: 38.7002
    - type: nauc_recall_at_5_max
      value: 39.6139
    - type: nauc_recall_at_5_std
      value: 8.362
    - type: nauc_recall_at_5_diff1
      value: 37.585
    - type: nauc_recall_at_10_max
      value: 39.2011
    - type: nauc_recall_at_10_std
      value: 15.155899999999999
    - type: nauc_recall_at_10_diff1
      value: 36.005199999999995
    - type: nauc_recall_at_20_max
      value: 40.221000000000004
    - type: nauc_recall_at_20_std
      value: 20.6873
    - type: nauc_recall_at_20_diff1
      value: 30.7941
    - type: nauc_recall_at_100_max
      value: 51.409800000000004
    - type: nauc_recall_at_100_std
      value: 46.4559
    - type: nauc_recall_at_100_diff1
      value: 35.7367
    - type: nauc_recall_at_1000_max
      value: 58.719500000000004
    - type: nauc_recall_at_1000_std
      value: 72.0053
    - type: nauc_recall_at_1000_diff1
      value: 36.0514
    - type: nauc_precision_at_1_max
      value: 44.5645
    - type: nauc_precision_at_1_std
      value: 4.542800000000001
    - type: nauc_precision_at_1_diff1
      value: 50.2359
    - type: nauc_precision_at_3_max
      value: 42.7363
    - type: nauc_precision_at_3_std
      value: 11.9582
    - type: nauc_precision_at_3_diff1
      value: 28.242800000000003
    - type: nauc_precision_at_5_max
      value: 39.7422
    - type: nauc_precision_at_5_std
      value: 16.2831
    - type: nauc_precision_at_5_diff1
      value: 21.6264
    - type: nauc_precision_at_10_max
      value: 33.4757
    - type: nauc_precision_at_10_std
      value: 18.8123
    - type: nauc_precision_at_10_diff1
      value: 14.122000000000002
    - type: nauc_precision_at_20_max
      value: 27.897
    - type: nauc_precision_at_20_std
      value: 17.7175
    - type: nauc_precision_at_20_diff1
      value: 4.8417
    - type: nauc_precision_at_100_max
      value: 16.4521
    - type: nauc_precision_at_100_std
      value: 15.6333
    - type: nauc_precision_at_100_diff1
      value: -3.7706999999999997
    - type: nauc_precision_at_1000_max
      value: 1.0215999999999998
    - type: nauc_precision_at_1000_std
      value: 1.7413
    - type: nauc_precision_at_1000_diff1
      value: -13.7539
    - type: nauc_mrr_at_1_max
      value: 44.5645
    - type: nauc_mrr_at_1_std
      value: 4.542800000000001
    - type: nauc_mrr_at_1_diff1
      value: 50.2359
    - type: nauc_mrr_at_3_max
      value: 46.611999999999995
    - type: nauc_mrr_at_3_std
      value: 7.647900000000001
    - type: nauc_mrr_at_3_diff1
      value: 45.3343
    - type: nauc_mrr_at_5_max
      value: 46.3141
    - type: nauc_mrr_at_5_std
      value: 7.9993
    - type: nauc_mrr_at_5_diff1
      value: 45.252900000000004
    - type: nauc_mrr_at_10_max
      value: 46.1605
    - type: nauc_mrr_at_10_std
      value: 8.6568
    - type: nauc_mrr_at_10_diff1
      value: 45.1293
    - type: nauc_mrr_at_20_max
      value: 46.1626
    - type: nauc_mrr_at_20_std
      value: 8.6536
    - type: nauc_mrr_at_20_diff1
      value: 45.0837
    - type: nauc_mrr_at_100_max
      value: 46.2514
    - type: nauc_mrr_at_100_std
      value: 8.731300000000001
    - type: nauc_mrr_at_100_diff1
      value: 45.2734
    - type: nauc_mrr_at_1000_max
      value: 46.2511
    - type: nauc_mrr_at_1000_std
      value: 8.6858
    - type: nauc_mrr_at_1000_diff1
      value: 45.29
    - type: main_score
      value: 48.742999999999995
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackRetrieval (default)
      revision: 160c094312a0e1facb97e55eeddb698c0abe3571
      split: test
      type: CQADupstackRetrieval_is_a_combined_dataset
    metrics:
    - type: ndcg_at_1
      value: 36.5025
    - type: ndcg_at_3
      value: 42.563833333333335
    - type: ndcg_at_5
      value: 45.190500000000014
    - type: ndcg_at_10
      value: 48.15416666666666
    - type: ndcg_at_20
      value: 50.29141666666666
    - type: ndcg_at_100
      value: 53.34008333333333
    - type: ndcg_at_1000
      value: 55.072416666666676
    - type: map_at_1
      value: 30.718333333333337
    - type: map_at_3
      value: 38.537166666666664
    - type: map_at_5
      value: 40.46825
    - type: map_at_10
      value: 42.020250000000004
    - type: map_at_20
      value: 42.783
    - type: map_at_100
      value: 43.36233333333334
    - type: map_at_1000
      value: 43.46825
    - type: recall_at_1
      value: 30.718333333333337
    - type: recall_at_3
      value: 46.2075
    - type: recall_at_5
      value: 52.98616666666667
    - type: recall_at_10
      value: 61.78366666666667
    - type: recall_at_20
      value: 69.50683333333333
    - type: recall_at_100
      value: 84.0005
    - type: recall_at_1000
      value: 95.623
    - type: precision_at_1
      value: 36.5025
    - type: precision_at_3
      value: 19.820999999999998
    - type: precision_at_5
      value: 14.119666666666669
    - type: precision_at_10
      value: 8.606083333333334
    - type: precision_at_20
      value: 5.0425
    - type: precision_at_100
      value: 1.3245
    - type: precision_at_1000
      value: 0.16624999999999998
    - type: mrr_at_1
      value: 36.50251666666667
    - type: mrr_at_3
      value: 43.639925000000005
    - type: mrr_at_5
      value: 45.17450833333333
    - type: mrr_at_10
      value: 46.29196666666667
    - type: mrr_at_20
      value: 46.787433333333325
    - type: mrr_at_100
      value: 47.11775833333334
    - type: mrr_at_1000
      value: 47.160025
    - type: nauc_ndcg_at_1_max
      value: 35.63543333333333
    - type: nauc_ndcg_at_1_std
      value: -2.5082500000000003
    - type: nauc_ndcg_at_1_diff1
      value: 49.697575
    - type: nauc_ndcg_at_3_max
      value: 34.4362
    - type: nauc_ndcg_at_3_std
      value: -1.8411749999999998
    - type: nauc_ndcg_at_3_diff1
      value: 43.73903333333333
    - type: nauc_ndcg_at_5_max
      value: 34.93775
    - type: nauc_ndcg_at_5_std
      value: -0.8254249999999997
    - type: nauc_ndcg_at_5_diff1
      value: 43.07621666666667
    - type: nauc_ndcg_at_10_max
      value: 35.32053333333333
    - type: nauc_ndcg_at_10_std
      value: 0.5296166666666667
    - type: nauc_ndcg_at_10_diff1
      value: 42.7897
    - type: nauc_ndcg_at_20_max
      value: 35.781600000000005
    - type: nauc_ndcg_at_20_std
      value: 1.3973583333333335
    - type: nauc_ndcg_at_20_diff1
      value: 42.563583333333334
    - type: nauc_ndcg_at_100_max
      value: 36.46264166666666
    - type: nauc_ndcg_at_100_std
      value: 2.793141666666667
    - type: nauc_ndcg_at_100_diff1
      value: 42.913475
    - type: nauc_ndcg_at_1000_max
      value: 36.389716666666665
    - type: nauc_ndcg_at_1000_std
      value: 2.1062499999999997
    - type: nauc_ndcg_at_1000_diff1
      value: 43.32690000000001
    - type: nauc_map_at_1_max
      value: 30.19065
    - type: nauc_map_at_1_std
      value: -6.136941666666667
    - type: nauc_map_at_1_diff1
      value: 50.95858333333334
    - type: nauc_map_at_3_max
      value: 32.65271666666666
    - type: nauc_map_at_3_std
      value: -3.927191666666667
    - type: nauc_map_at_3_diff1
      value: 45.89055
    - type: nauc_map_at_5_max
      value: 33.56583333333334
    - type: nauc_map_at_5_std
      value: -2.8991750000000005
    - type: nauc_map_at_5_diff1
      value: 45.29093333333334
    - type: nauc_map_at_10_max
      value: 34.177641666666666
    - type: nauc_map_at_10_std
      value: -1.9589083333333333
    - type: nauc_map_at_10_diff1
      value: 45.126108333333335
    - type: nauc_map_at_20_max
      value: 34.461074999999994
    - type: nauc_map_at_20_std
      value: -1.550616666666666
    - type: nauc_map_at_20_diff1
      value: 45.00503333333333
    - type: nauc_map_at_100_max
      value: 34.69629166666666
    - type: nauc_map_at_100_std
      value: -1.1661166666666671
    - type: nauc_map_at_100_diff1
      value: 45.009175
    - type: nauc_map_at_1000_max
      value: 34.688108333333325
    - type: nauc_map_at_1000_std
      value: -1.1726583333333331
    - type: nauc_map_at_1000_diff1
      value: 45.010266666666666
    - type: nauc_recall_at_1_max
      value: 30.19065
    - type: nauc_recall_at_1_std
      value: -6.136941666666667
    - type: nauc_recall_at_1_diff1
      value: 50.95858333333334
    - type: nauc_recall_at_3_max
      value: 31.18069166666666
    - type: nauc_recall_at_3_std
      value: -2.425375
    - type: nauc_recall_at_3_diff1
      value: 39.215491666666665
    - type: nauc_recall_at_5_max
      value: 32.40545833333333
    - type: nauc_recall_at_5_std
      value: 0.30784166666666674
    - type: nauc_recall_at_5_diff1
      value: 36.58546666666667
    - type: nauc_recall_at_10_max
      value: 33.11824166666668
    - type: nauc_recall_at_10_std
      value: 5.099150000000001
    - type: nauc_recall_at_10_diff1
      value: 34.32635833333333
    - type: nauc_recall_at_20_max
      value: 34.84125
    - type: nauc_recall_at_20_std
      value: 9.744425
    - type: nauc_recall_at_20_diff1
      value: 32.073550000000004
    - type: nauc_recall_at_100_max
      value: 40.07125
    - type: nauc_recall_at_100_std
      value: 26.520391666666672
    - type: nauc_recall_at_100_diff1
      value: 29.73679166666667
    - type: nauc_recall_at_1000_max
      value: 52.596025000000004
    - type: nauc_recall_at_1000_std
      value: 53.16131666666667
    - type: nauc_recall_at_1000_diff1
      value: 27.2596
    - type: nauc_precision_at_1_max
      value: 35.63543333333333
    - type: nauc_precision_at_1_std
      value: -2.5082500000000003
    - type: nauc_precision_at_1_diff1
      value: 49.697575
    - type: nauc_precision_at_3_max
      value: 34.383424999999995
    - type: nauc_precision_at_3_std
      value: 4.906383333333332
    - type: nauc_precision_at_3_diff1
      value: 27.956991666666664
    - type: nauc_precision_at_5_max
      value: 33.50664166666667
    - type: nauc_precision_at_5_std
      value: 9.5448
    - type: nauc_precision_at_5_diff1
      value: 20.584491666666665
    - type: nauc_precision_at_10_max
      value: 30.116449999999993
    - type: nauc_precision_at_10_std
      value: 14.272133333333334
    - type: nauc_precision_at_10_diff1
      value: 12.496183333333333
    - type: nauc_precision_at_20_max
      value: 26.383483333333334
    - type: nauc_precision_at_20_std
      value: 16.945558333333334
    - type: nauc_precision_at_20_diff1
      value: 5.616483333333333
    - type: nauc_precision_at_100_max
      value: 17.88254166666667
    - type: nauc_precision_at_100_std
      value: 19.543916666666668
    - type: nauc_precision_at_100_diff1
      value: -4.408391666666666
    - type: nauc_precision_at_1000_max
      value: 6.492849999999999
    - type: nauc_precision_at_1000_std
      value: 11.98045
    - type: nauc_precision_at_1000_diff1
      value: -12.374983333333333
    - type: nauc_mrr_at_1_max
      value: 35.63543333333333
    - type: nauc_mrr_at_1_std
      value: -2.5082500000000003
    - type: nauc_mrr_at_1_diff1
      value: 49.697575
    - type: nauc_mrr_at_3_max
      value: 36.531841666666665
    - type: nauc_mrr_at_3_std
      value: -0.49094999999999983
    - type: nauc_mrr_at_3_diff1
      value: 45.05095
    - type: nauc_mrr_at_5_max
      value: 36.68914166666667
    - type: nauc_mrr_at_5_std
      value: -0.020883333333333517
    - type: nauc_mrr_at_5_diff1
      value: 44.59794166666667
    - type: nauc_mrr_at_10_max
      value: 36.71131666666667
    - type: nauc_mrr_at_10_std
      value: 0.42916666666666675
    - type: nauc_mrr_at_10_diff1
      value: 44.502241666666656
    - type: nauc_mrr_at_20_max
      value: 36.73486666666667
    - type: nauc_mrr_at_20_std
      value: 0.5398083333333334
    - type: nauc_mrr_at_20_diff1
      value: 44.48308333333335
    - type: nauc_mrr_at_100_max
      value: 36.76240833333333
    - type: nauc_mrr_at_100_std
      value: 0.6035583333333332
    - type: nauc_mrr_at_100_diff1
      value: 44.55041666666667
    - type: nauc_mrr_at_1000_max
      value: 36.76164166666667
    - type: nauc_mrr_at_1000_std
      value: 0.5883499999999998
    - type: nauc_mrr_at_1000_diff1
      value: 44.56814166666667
    - type: main_score
      value: 48.15416666666666
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackRetrieval (default)
      revision: CQADupstackRetrieval_is_a_combined_dataset
      split: test
      type: CQADupstackRetrieval_is_a_combined_dataset
    metrics:
    - type: main_score
      value: 48.15416666666667
    - type: ndcg_at_10
      value: 48.15416666666667
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackStatsRetrieval (default)
      revision: 65ac3a16b8e91f9cee4c9828cc7c335575432a2a
      split: test
      type: mteb/cqadupstack-stats
    metrics:
    - type: ndcg_at_1
      value: 32.669
    - type: ndcg_at_3
      value: 37.604
    - type: ndcg_at_5
      value: 39.682
    - type: ndcg_at_10
      value: 42.353
    - type: ndcg_at_20
      value: 44.374
    - type: ndcg_at_100
      value: 47.424
    - type: ndcg_at_1000
      value: 49.589
    - type: map_at_1
      value: 29.193
    - type: map_at_3
      value: 34.897
    - type: map_at_5
      value: 36.272999999999996
    - type: map_at_10
      value: 37.529
    - type: map_at_20
      value: 38.156
    - type: map_at_100
      value: 38.614
    - type: map_at_1000
      value: 38.712999999999994
    - type: recall_at_1
      value: 29.193
    - type: recall_at_3
      value: 41.014
    - type: recall_at_5
      value: 46.248
    - type: recall_at_10
      value: 54.159
    - type: recall_at_20
      value: 61.818
    - type: recall_at_100
      value: 77.267
    - type: recall_at_1000
      value: 92.805
    - type: precision_at_1
      value: 32.669
    - type: precision_at_3
      value: 16.309
    - type: precision_at_5
      value: 11.288
    - type: precision_at_10
      value: 6.8709999999999996
    - type: precision_at_20
      value: 3.9419999999999997
    - type: precision_at_100
      value: 1.008
    - type: precision_at_1000
      value: 0.126
    - type: mrr_at_1
      value: 32.6687
    - type: mrr_at_3
      value: 38.0368
    - type: mrr_at_5
      value: 39.1948
    - type: mrr_at_10
      value: 40.2884
    - type: mrr_at_20
      value: 40.7986
    - type: mrr_at_100
      value: 41.1771
    - type: mrr_at_1000
      value: 41.240700000000004
    - type: nauc_ndcg_at_1_max
      value: 38.765699999999995
    - type: nauc_ndcg_at_1_std
      value: 3.3594
    - type: nauc_ndcg_at_1_diff1
      value: 54.1068
    - type: nauc_ndcg_at_3_max
      value: 35.987700000000004
    - type: nauc_ndcg_at_3_std
      value: 2.8396999999999997
    - type: nauc_ndcg_at_3_diff1
      value: 47.2858
    - type: nauc_ndcg_at_5_max
      value: 36.628699999999995
    - type: nauc_ndcg_at_5_std
      value: 3.6117000000000004
    - type: nauc_ndcg_at_5_diff1
      value: 46.9776
    - type: nauc_ndcg_at_10_max
      value: 36.763200000000005
    - type: nauc_ndcg_at_10_std
      value: 4.7951
    - type: nauc_ndcg_at_10_diff1
      value: 46.5066
    - type: nauc_ndcg_at_20_max
      value: 36.6793
    - type: nauc_ndcg_at_20_std
      value: 5.6449
    - type: nauc_ndcg_at_20_diff1
      value: 45.835100000000004
    - type: nauc_ndcg_at_100_max
      value: 37.0064
    - type: nauc_ndcg_at_100_std
      value: 6.6625000000000005
    - type: nauc_ndcg_at_100_diff1
      value: 45.4937
    - type: nauc_ndcg_at_1000_max
      value: 37.5693
    - type: nauc_ndcg_at_1000_std
      value: 6.5411
    - type: nauc_ndcg_at_1000_diff1
      value: 46.671800000000005
    - type: nauc_map_at_1_max
      value: 32.7625
    - type: nauc_map_at_1_std
      value: -1.8726
    - type: nauc_map_at_1_diff1
      value: 53.1931
    - type: nauc_map_at_3_max
      value: 34.7221
    - type: nauc_map_at_3_std
      value: 1.141
    - type: nauc_map_at_3_diff1
      value: 49.0672
    - type: nauc_map_at_5_max
      value: 35.5173
    - type: nauc_map_at_5_std
      value: 2.2872
    - type: nauc_map_at_5_diff1
      value: 48.5047
    - type: nauc_map_at_10_max
      value: 35.7686
    - type: nauc_map_at_10_std
      value: 2.9238
    - type: nauc_map_at_10_diff1
      value: 48.3548
    - type: nauc_map_at_20_max
      value: 35.7707
    - type: nauc_map_at_20_std
      value: 3.0683
    - type: nauc_map_at_20_diff1
      value: 48.1708
    - type: nauc_map_at_100_max
      value: 35.8572
    - type: nauc_map_at_100_std
      value: 3.2108999999999996
    - type: nauc_map_at_100_diff1
      value: 48.0681
    - type: nauc_map_at_1000_max
      value: 35.885600000000004
    - type: nauc_map_at_1000_std
      value: 3.2162
    - type: nauc_map_at_1000_diff1
      value: 48.1239
    - type: nauc_recall_at_1_max
      value: 32.7625
    - type: nauc_recall_at_1_std
      value: -1.8726
    - type: nauc_recall_at_1_diff1
      value: 53.1931
    - type: nauc_recall_at_3_max
      value: 32.5847
    - type: nauc_recall_at_3_std
      value: 1.4236
    - type: nauc_recall_at_3_diff1
      value: 42.8899
    - type: nauc_recall_at_5_max
      value: 35.0441
    - type: nauc_recall_at_5_std
      value: 4.1737
    - type: nauc_recall_at_5_diff1
      value: 41.8313
    - type: nauc_recall_at_10_max
      value: 35.063100000000006
    - type: nauc_recall_at_10_std
      value: 7.8740000000000006
    - type: nauc_recall_at_10_diff1
      value: 38.9244
    - type: nauc_recall_at_20_max
      value: 33.6964
    - type: nauc_recall_at_20_std
      value: 12.0632
    - type: nauc_recall_at_20_diff1
      value: 34.7941
    - type: nauc_recall_at_100_max
      value: 33.928399999999996
    - type: nauc_recall_at_100_std
      value: 23.1451
    - type: nauc_recall_at_100_diff1
      value: 28.170499999999997
    - type: nauc_recall_at_1000_max
      value: 45.6188
    - type: nauc_recall_at_1000_std
      value: 44.1766
    - type: nauc_recall_at_1000_diff1
      value: 34.1945
    - type: nauc_precision_at_1_max
      value: 38.765699999999995
    - type: nauc_precision_at_1_std
      value: 3.3594
    - type: nauc_precision_at_1_diff1
      value: 54.1068
    - type: nauc_precision_at_3_max
      value: 39.3932
    - type: nauc_precision_at_3_std
      value: 11.258600000000001
    - type: nauc_precision_at_3_diff1
      value: 36.9186
    - type: nauc_precision_at_5_max
      value: 39.0844
    - type: nauc_precision_at_5_std
      value: 14.7369
    - type: nauc_precision_at_5_diff1
      value: 31.3071
    - type: nauc_precision_at_10_max
      value: 36.3678
    - type: nauc_precision_at_10_std
      value: 17.292099999999998
    - type: nauc_precision_at_10_diff1
      value: 24.0674
    - type: nauc_precision_at_20_max
      value: 32.5422
    - type: nauc_precision_at_20_std
      value: 17.3521
    - type: nauc_precision_at_20_diff1
      value: 17.8472
    - type: nauc_precision_at_100_max
      value: 28.439700000000002
    - type: nauc_precision_at_100_std
      value: 21.7441
    - type: nauc_precision_at_100_diff1
      value: 7.6072
    - type: nauc_precision_at_1000_max
      value: 18.9222
    - type: nauc_precision_at_1000_std
      value: 17.1045
    - type: nauc_precision_at_1000_diff1
      value: 0.9424
    - type: nauc_mrr_at_1_max
      value: 38.765699999999995
    - type: nauc_mrr_at_1_std
      value: 3.3594
    - type: nauc_mrr_at_1_diff1
      value: 54.1068
    - type: nauc_mrr_at_3_max
      value: 38.4312
    - type: nauc_mrr_at_3_std
      value: 4.4437999999999995
    - type: nauc_mrr_at_3_diff1
      value: 49.0981
    - type: nauc_mrr_at_5_max
      value: 38.8429
    - type: nauc_mrr_at_5_std
      value: 4.7834
    - type: nauc_mrr_at_5_diff1
      value: 49.1564
    - type: nauc_mrr_at_10_max
      value: 39.1657
    - type: nauc_mrr_at_10_std
      value: 5.3785
    - type: nauc_mrr_at_10_diff1
      value: 49.0301
    - type: nauc_mrr_at_20_max
      value: 39.1254
    - type: nauc_mrr_at_20_std
      value: 5.6123
    - type: nauc_mrr_at_20_diff1
      value: 48.8663
    - type: nauc_mrr_at_100_max
      value: 39.097
    - type: nauc_mrr_at_100_std
      value: 5.6065
    - type: nauc_mrr_at_100_diff1
      value: 48.827799999999996
    - type: nauc_mrr_at_1000_max
      value: 39.1157
    - type: nauc_mrr_at_1000_std
      value: 5.6175999999999995
    - type: nauc_mrr_at_1000_diff1
      value: 48.8575
    - type: main_score
      value: 42.353
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackTexRetrieval (default)
      revision: 46989137a86843e03a6195de44b09deda022eec7
      split: test
      type: mteb/cqadupstack-tex
    metrics:
    - type: ndcg_at_1
      value: 25.946
    - type: ndcg_at_3
      value: 31.463
    - type: ndcg_at_5
      value: 33.803
    - type: ndcg_at_10
      value: 36.55
    - type: ndcg_at_20
      value: 38.794000000000004
    - type: ndcg_at_100
      value: 42.327999999999996
    - type: ndcg_at_1000
      value: 44.783
    - type: map_at_1
      value: 21.217
    - type: map_at_3
      value: 27.882
    - type: map_at_5
      value: 29.537000000000003
    - type: map_at_10
      value: 30.848
    - type: map_at_20
      value: 31.574999999999996
    - type: map_at_100
      value: 32.173
    - type: map_at_1000
      value: 32.296
    - type: recall_at_1
      value: 21.217
    - type: recall_at_3
      value: 34.993
    - type: recall_at_5
      value: 41.028999999999996
    - type: recall_at_10
      value: 49.327
    - type: recall_at_20
      value: 57.50300000000001
    - type: recall_at_100
      value: 74.72
    - type: recall_at_1000
      value: 91.637
    - type: precision_at_1
      value: 25.946
    - type: precision_at_3
      value: 15.129999999999999
    - type: precision_at_5
      value: 10.991
    - type: precision_at_10
      value: 6.793
    - type: precision_at_20
      value: 4.076
    - type: precision_at_100
      value: 1.138
    - type: precision_at_1000
      value: 0.155
    - type: mrr_at_1
      value: 25.9463
    - type: mrr_at_3
      value: 32.4845
    - type: mrr_at_5
      value: 33.9642
    - type: mrr_at_10
      value: 35.0906
    - type: mrr_at_20
      value: 35.6346
    - type: mrr_at_100
      value: 36.0474
    - type: mrr_at_1000
      value: 36.1106
    - type: nauc_ndcg_at_1_max
      value: 29.3294
    - type: nauc_ndcg_at_1_std
      value: 1.9199000000000002
    - type: nauc_ndcg_at_1_diff1
      value: 43.9951
    - type: nauc_ndcg_at_3_max
      value: 28.4154
    - type: nauc_ndcg_at_3_std
      value: 2.262
    - type: nauc_ndcg_at_3_diff1
      value: 37.0416
    - type: nauc_ndcg_at_5_max
      value: 29.0647
    - type: nauc_ndcg_at_5_std
      value: 3.6863
    - type: nauc_ndcg_at_5_diff1
      value: 36.3715
    - type: nauc_ndcg_at_10_max
      value: 29.0041
    - type: nauc_ndcg_at_10_std
      value: 4.605
    - type: nauc_ndcg_at_10_diff1
      value: 36.1295
    - type: nauc_ndcg_at_20_max
      value: 29.5425
    - type: nauc_ndcg_at_20_std
      value: 5.5535
    - type: nauc_ndcg_at_20_diff1
      value: 35.74
    - type: nauc_ndcg_at_100_max
      value: 30.1166
    - type: nauc_ndcg_at_100_std
      value: 7.4285000000000005
    - type: nauc_ndcg_at_100_diff1
      value: 35.4871
    - type: nauc_ndcg_at_1000_max
      value: 30.198900000000002
    - type: nauc_ndcg_at_1000_std
      value: 6.6549
    - type: nauc_ndcg_at_1000_diff1
      value: 36.3901
    - type: nauc_map_at_1_max
      value: 26.6761
    - type: nauc_map_at_1_std
      value: -0.4332
    - type: nauc_map_at_1_diff1
      value: 46.015299999999996
    - type: nauc_map_at_3_max
      value: 27.221
    - type: nauc_map_at_3_std
      value: 1.3299999999999998
    - type: nauc_map_at_3_diff1
      value: 38.9882
    - type: nauc_map_at_5_max
      value: 27.929900000000004
    - type: nauc_map_at_5_std
      value: 2.1886
    - type: nauc_map_at_5_diff1
      value: 38.5184
    - type: nauc_map_at_10_max
      value: 28.105599999999995
    - type: nauc_map_at_10_std
      value: 2.6707
    - type: nauc_map_at_10_diff1
      value: 38.419599999999996
    - type: nauc_map_at_20_max
      value: 28.359499999999997
    - type: nauc_map_at_20_std
      value: 2.9859
    - type: nauc_map_at_20_diff1
      value: 38.2748
    - type: nauc_map_at_100_max
      value: 28.5493
    - type: nauc_map_at_100_std
      value: 3.3446999999999996
    - type: nauc_map_at_100_diff1
      value: 38.1789
    - type: nauc_map_at_1000_max
      value: 28.5931
    - type: nauc_map_at_1000_std
      value: 3.3341999999999996
    - type: nauc_map_at_1000_diff1
      value: 38.2276
    - type: nauc_recall_at_1_max
      value: 26.6761
    - type: nauc_recall_at_1_std
      value: -0.4332
    - type: nauc_recall_at_1_diff1
      value: 46.015299999999996
    - type: nauc_recall_at_3_max
      value: 26.0116
    - type: nauc_recall_at_3_std
      value: 2.6044
    - type: nauc_recall_at_3_diff1
      value: 32.1201
    - type: nauc_recall_at_5_max
      value: 27.361
    - type: nauc_recall_at_5_std
      value: 5.6135
    - type: nauc_recall_at_5_diff1
      value: 29.807699999999997
    - type: nauc_recall_at_10_max
      value: 26.885399999999997
    - type: nauc_recall_at_10_std
      value: 8.1679
    - type: nauc_recall_at_10_diff1
      value: 28.283599999999996
    - type: nauc_recall_at_20_max
      value: 28.5827
    - type: nauc_recall_at_20_std
      value: 11.7346
    - type: nauc_recall_at_20_diff1
      value: 25.965
    - type: nauc_recall_at_100_max
      value: 31.488100000000003
    - type: nauc_recall_at_100_std
      value: 25.9126
    - type: nauc_recall_at_100_diff1
      value: 20.9561
    - type: nauc_recall_at_1000_max
      value: 37.424
    - type: nauc_recall_at_1000_std
      value: 35.7201
    - type: nauc_recall_at_1000_diff1
      value: 22.156100000000002
    - type: nauc_precision_at_1_max
      value: 29.3294
    - type: nauc_precision_at_1_std
      value: 1.9199000000000002
    - type: nauc_precision_at_1_diff1
      value: 43.9951
    - type: nauc_precision_at_3_max
      value: 29.893700000000003
    - type: nauc_precision_at_3_std
      value: 5.0083
    - type: nauc_precision_at_3_diff1
      value: 28.530499999999996
    - type: nauc_precision_at_5_max
      value: 30.6624
    - type: nauc_precision_at_5_std
      value: 8.098600000000001
    - type: nauc_precision_at_5_diff1
      value: 23.8478
    - type: nauc_precision_at_10_max
      value: 28.407100000000003
    - type: nauc_precision_at_10_std
      value: 10.852599999999999
    - type: nauc_precision_at_10_diff1
      value: 19.1175
    - type: nauc_precision_at_20_max
      value: 26.045299999999997
    - type: nauc_precision_at_20_std
      value: 12.898399999999999
    - type: nauc_precision_at_20_diff1
      value: 13.586599999999999
    - type: nauc_precision_at_100_max
      value: 23.8686
    - type: nauc_precision_at_100_std
      value: 16.558500000000002
    - type: nauc_precision_at_100_diff1
      value: 4.8838
    - type: nauc_precision_at_1000_max
      value: 18.803900000000002
    - type: nauc_precision_at_1000_std
      value: 8.252600000000001
    - type: nauc_precision_at_1000_diff1
      value: 3.4761
    - type: nauc_mrr_at_1_max
      value: 29.3294
    - type: nauc_mrr_at_1_std
      value: 1.9199000000000002
    - type: nauc_mrr_at_1_diff1
      value: 43.9951
    - type: nauc_mrr_at_3_max
      value: 29.7689
    - type: nauc_mrr_at_3_std
      value: 2.9381
    - type: nauc_mrr_at_3_diff1
      value: 39.0616
    - type: nauc_mrr_at_5_max
      value: 30.0871
    - type: nauc_mrr_at_5_std
      value: 3.7067
    - type: nauc_mrr_at_5_diff1
      value: 38.2429
    - type: nauc_mrr_at_10_max
      value: 30.0444
    - type: nauc_mrr_at_10_std
      value: 4.086399999999999
    - type: nauc_mrr_at_10_diff1
      value: 38.0941
    - type: nauc_mrr_at_20_max
      value: 30.134499999999996
    - type: nauc_mrr_at_20_std
      value: 4.288200000000001
    - type: nauc_mrr_at_20_diff1
      value: 38.048300000000005
    - type: nauc_mrr_at_100_max
      value: 30.1624
    - type: nauc_mrr_at_100_std
      value: 4.4486
    - type: nauc_mrr_at_100_diff1
      value: 38.067499999999995
    - type: nauc_mrr_at_1000_max
      value: 30.168899999999997
    - type: nauc_mrr_at_1000_std
      value: 4.4265
    - type: nauc_mrr_at_1000_diff1
      value: 38.0978
    - type: main_score
      value: 36.55
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackUnixRetrieval (default)
      revision: 6c6430d3a6d36f8d2a829195bc5dc94d7e063e53
      split: test
      type: mteb/cqadupstack-unix
    metrics:
    - type: ndcg_at_1
      value: 40.111999999999995
    - type: ndcg_at_3
      value: 44.91
    - type: ndcg_at_5
      value: 48.048
    - type: ndcg_at_10
      value: 51.300000000000004
    - type: ndcg_at_20
      value: 53.537
    - type: ndcg_at_100
      value: 56.53399999999999
    - type: ndcg_at_1000
      value: 58.048
    - type: map_at_1
      value: 34.303
    - type: map_at_3
      value: 41.43
    - type: map_at_5
      value: 43.633
    - type: map_at_10
      value: 45.312000000000005
    - type: map_at_20
      value: 46.04
    - type: map_at_100
      value: 46.563
    - type: map_at_1000
      value: 46.64
    - type: recall_at_1
      value: 34.303
    - type: recall_at_3
      value: 48.465
    - type: recall_at_5
      value: 56.374
    - type: recall_at_10
      value: 65.508
    - type: recall_at_20
      value: 73.457
    - type: recall_at_100
      value: 87.53
    - type: recall_at_1000
      value: 97.42
    - type: precision_at_1
      value: 40.111999999999995
    - type: precision_at_3
      value: 20.211000000000002
    - type: precision_at_5
      value: 14.496
    - type: precision_at_10
      value: 8.806
    - type: precision_at_20
      value: 5.047
    - type: precision_at_100
      value: 1.266
    - type: precision_at_1000
      value: 0.149
    - type: mrr_at_1
      value: 40.1119
    - type: mrr_at_3
      value: 46.1287
    - type: mrr_at_5
      value: 47.9011
    - type: mrr_at_10
      value: 49.0974
    - type: mrr_at_20
      value: 49.6541
    - type: mrr_at_100
      value: 49.9655
    - type: mrr_at_1000
      value: 50.0063
    - type: nauc_ndcg_at_1_max
      value: 40.5521
    - type: nauc_ndcg_at_1_std
      value: -7.457700000000001
    - type: nauc_ndcg_at_1_diff1
      value: 50.6505
    - type: nauc_ndcg_at_3_max
      value: 38.696999999999996
    - type: nauc_ndcg_at_3_std
      value: -4.2286
    - type: nauc_ndcg_at_3_diff1
      value: 44.289699999999996
    - type: nauc_ndcg_at_5_max
      value: 39.6798
    - type: nauc_ndcg_at_5_std
      value: -2.8316
    - type: nauc_ndcg_at_5_diff1
      value: 44.0944
    - type: nauc_ndcg_at_10_max
      value: 40.5534
    - type: nauc_ndcg_at_10_std
      value: -2.2217000000000002
    - type: nauc_ndcg_at_10_diff1
      value: 43.811299999999996
    - type: nauc_ndcg_at_20_max
      value: 41.1096
    - type: nauc_ndcg_at_20_std
      value: -1.5137
    - type: nauc_ndcg_at_20_diff1
      value: 43.7406
    - type: nauc_ndcg_at_100_max
      value: 40.588
    - type: nauc_ndcg_at_100_std
      value: -1.2616
    - type: nauc_ndcg_at_100_diff1
      value: 43.553
    - type: nauc_ndcg_at_1000_max
      value: 40.86
    - type: nauc_ndcg_at_1000_std
      value: -1.6507999999999998
    - type: nauc_ndcg_at_1000_diff1
      value: 44.1305
    - type: nauc_map_at_1_max
      value: 36.9173
    - type: nauc_map_at_1_std
      value: -8.2788
    - type: nauc_map_at_1_diff1
      value: 52.4203
    - type: nauc_map_at_3_max
      value: 38.006499999999996
    - type: nauc_map_at_3_std
      value: -5.5607
    - type: nauc_map_at_3_diff1
      value: 46.847
    - type: nauc_map_at_5_max
      value: 39.1588
    - type: nauc_map_at_5_std
      value: -4.6744
    - type: nauc_map_at_5_diff1
      value: 46.3773
    - type: nauc_map_at_10_max
      value: 39.8953
    - type: nauc_map_at_10_std
      value: -4.3361
    - type: nauc_map_at_10_diff1
      value: 46.1408
    - type: nauc_map_at_20_max
      value: 40.1053
    - type: nauc_map_at_20_std
      value: -4.1688
    - type: nauc_map_at_20_diff1
      value: 46.0601
    - type: nauc_map_at_100_max
      value: 40.0756
    - type: nauc_map_at_100_std
      value: -4.0973999999999995
    - type: nauc_map_at_100_diff1
      value: 46.0325
    - type: nauc_map_at_1000_max
      value: 40.0894
    - type: nauc_map_at_1000_std
      value: -4.0949
    - type: nauc_map_at_1000_diff1
      value: 46.048899999999996
    - type: nauc_recall_at_1_max
      value: 36.9173
    - type: nauc_recall_at_1_std
      value: -8.2788
    - type: nauc_recall_at_1_diff1
      value: 52.4203
    - type: nauc_recall_at_3_max
      value: 35.2291
    - type: nauc_recall_at_3_std
      value: -2.4944
    - type: nauc_recall_at_3_diff1
      value: 39.3066
    - type: nauc_recall_at_5_max
      value: 37.2859
    - type: nauc_recall_at_5_std
      value: 1.2917
    - type: nauc_recall_at_5_diff1
      value: 37.2158
    - type: nauc_recall_at_10_max
      value: 38.9748
    - type: nauc_recall_at_10_std
      value: 3.8526
    - type: nauc_recall_at_10_diff1
      value: 35.188
    - type: nauc_recall_at_20_max
      value: 41.1368
    - type: nauc_recall_at_20_std
      value: 8.1788
    - type: nauc_recall_at_20_diff1
      value: 33.8061
    - type: nauc_recall_at_100_max
      value: 36.280499999999996
    - type: nauc_recall_at_100_std
      value: 16.6693
    - type: nauc_recall_at_100_diff1
      value: 26.466
    - type: nauc_recall_at_1000_max
      value: 57.084999999999994
    - type: nauc_recall_at_1000_std
      value: 56.954499999999996
    - type: nauc_recall_at_1000_diff1
      value: 25.915300000000002
    - type: nauc_precision_at_1_max
      value: 40.5521
    - type: nauc_precision_at_1_std
      value: -7.457700000000001
    - type: nauc_precision_at_1_diff1
      value: 50.6505
    - type: nauc_precision_at_3_max
      value: 36.2259
    - type: nauc_precision_at_3_std
      value: 0.8514
    - type: nauc_precision_at_3_diff1
      value: 27.168300000000002
    - type: nauc_precision_at_5_max
      value: 35.6781
    - type: nauc_precision_at_5_std
      value: 5.119400000000001
    - type: nauc_precision_at_5_diff1
      value: 19.7828
    - type: nauc_precision_at_10_max
      value: 29.9623
    - type: nauc_precision_at_10_std
      value: 6.7059
    - type: nauc_precision_at_10_diff1
      value: 9.7104
    - type: nauc_precision_at_20_max
      value: 26.2428
    - type: nauc_precision_at_20_std
      value: 9.854000000000001
    - type: nauc_precision_at_20_diff1
      value: 2.6679999999999997
    - type: nauc_precision_at_100_max
      value: 9.9456
    - type: nauc_precision_at_100_std
      value: 12.465
    - type: nauc_precision_at_100_diff1
      value: -11.0348
    - type: nauc_precision_at_1000_max
      value: -3.3062
    - type: nauc_precision_at_1000_std
      value: 5.3786000000000005
    - type: nauc_precision_at_1000_diff1
      value: -18.712999999999997
    - type: nauc_mrr_at_1_max
      value: 40.5521
    - type: nauc_mrr_at_1_std
      value: -7.457700000000001
    - type: nauc_mrr_at_1_diff1
      value: 50.6505
    - type: nauc_mrr_at_3_max
      value: 39.994
    - type: nauc_mrr_at_3_std
      value: -4.4112
    - type: nauc_mrr_at_3_diff1
      value: 45.0963
    - type: nauc_mrr_at_5_max
      value: 40.3926
    - type: nauc_mrr_at_5_std
      value: -3.611
    - type: nauc_mrr_at_5_diff1
      value: 44.9505
    - type: nauc_mrr_at_10_max
      value: 40.597
    - type: nauc_mrr_at_10_std
      value: -3.5407
    - type: nauc_mrr_at_10_diff1
      value: 45.0605
    - type: nauc_mrr_at_20_max
      value: 40.6821
    - type: nauc_mrr_at_20_std
      value: -3.4132000000000002
    - type: nauc_mrr_at_20_diff1
      value: 45.1507
    - type: nauc_mrr_at_100_max
      value: 40.6279
    - type: nauc_mrr_at_100_std
      value: -3.4576000000000002
    - type: nauc_mrr_at_100_diff1
      value: 45.183299999999996
    - type: nauc_mrr_at_1000_max
      value: 40.6436
    - type: nauc_mrr_at_1000_std
      value: -3.4639
    - type: nauc_mrr_at_1000_diff1
      value: 45.2065
    - type: main_score
      value: 51.300000000000004
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackWebmastersRetrieval (default)
      revision: 160c094312a0e1facb97e55eeddb698c0abe3571
      split: test
      type: mteb/cqadupstack-webmasters
    metrics:
    - type: ndcg_at_1
      value: 36.364000000000004
    - type: ndcg_at_3
      value: 41.875
    - type: ndcg_at_5
      value: 44.316
    - type: ndcg_at_10
      value: 47.301
    - type: ndcg_at_20
      value: 50.059
    - type: ndcg_at_100
      value: 53.698
    - type: ndcg_at_1000
      value: 55.503
    - type: map_at_1
      value: 30.312
    - type: map_at_3
      value: 37.527
    - type: map_at_5
      value: 39.36
    - type: map_at_10
      value: 40.931
    - type: map_at_20
      value: 41.978
    - type: map_at_100
      value: 42.893
    - type: map_at_1000
      value: 43.120000000000005
    - type: recall_at_1
      value: 30.312
    - type: recall_at_3
      value: 44.251000000000005
    - type: recall_at_5
      value: 50.456999999999994
    - type: recall_at_10
      value: 59.418000000000006
    - type: recall_at_20
      value: 69.791
    - type: recall_at_100
      value: 86.56
    - type: recall_at_1000
      value: 97.41199999999999
    - type: precision_at_1
      value: 36.364000000000004
    - type: precision_at_3
      value: 19.499
    - type: precision_at_5
      value: 14.149999999999999
    - type: precision_at_10
      value: 9.032
    - type: precision_at_20
      value: 5.800000000000001
    - type: precision_at_100
      value: 1.806
    - type: precision_at_1000
      value: 0.258
    - type: mrr_at_1
      value: 36.3636
    - type: mrr_at_3
      value: 42.918299999999995
    - type: mrr_at_5
      value: 44.4302
    - type: mrr_at_10
      value: 45.677299999999995
    - type: mrr_at_20
      value: 46.372600000000006
    - type: mrr_at_100
      value: 46.7532
    - type: mrr_at_1000
      value: 46.786699999999996
    - type: nauc_ndcg_at_1_max
      value: 36.5416
    - type: nauc_ndcg_at_1_std
      value: 1.7398
    - type: nauc_ndcg_at_1_diff1
      value: 48.6149
    - type: nauc_ndcg_at_3_max
      value: 35.9768
    - type: nauc_ndcg_at_3_std
      value: 4.3271999999999995
    - type: nauc_ndcg_at_3_diff1
      value: 43.4812
    - type: nauc_ndcg_at_5_max
      value: 34.9136
    - type: nauc_ndcg_at_5_std
      value: 5.291300000000001
    - type: nauc_ndcg_at_5_diff1
      value: 42.4122
    - type: nauc_ndcg_at_10_max
      value: 35.3659
    - type: nauc_ndcg_at_10_std
      value: 6.8223
    - type: nauc_ndcg_at_10_diff1
      value: 42.123
    - type: nauc_ndcg_at_20_max
      value: 37.302400000000006
    - type: nauc_ndcg_at_20_std
      value: 7.836600000000001
    - type: nauc_ndcg_at_20_diff1
      value: 42.9609
    - type: nauc_ndcg_at_100_max
      value: 38.028800000000004
    - type: nauc_ndcg_at_100_std
      value: 9.065900000000001
    - type: nauc_ndcg_at_100_diff1
      value: 42.8557
    - type: nauc_ndcg_at_1000_max
      value: 37.8805
    - type: nauc_ndcg_at_1000_std
      value: 7.965800000000001
    - type: nauc_ndcg_at_1000_diff1
      value: 43.331399999999995
    - type: nauc_map_at_1_max
      value: 32.5587
    - type: nauc_map_at_1_std
      value: -2.3119
    - type: nauc_map_at_1_diff1
      value: 52.2244
    - type: nauc_map_at_3_max
      value: 34.6582
    - type: nauc_map_at_3_std
      value: 1.3005
    - type: nauc_map_at_3_diff1
      value: 46.774100000000004
    - type: nauc_map_at_5_max
      value: 34.6492
    - type: nauc_map_at_5_std
      value: 2.2614
    - type: nauc_map_at_5_diff1
      value: 45.9467
    - type: nauc_map_at_10_max
      value: 35.4443
    - type: nauc_map_at_10_std
      value: 3.7047999999999996
    - type: nauc_map_at_10_diff1
      value: 45.6336
    - type: nauc_map_at_20_max
      value: 36.1327
    - type: nauc_map_at_20_std
      value: 4.3156
    - type: nauc_map_at_20_diff1
      value: 45.7802
    - type: nauc_map_at_100_max
      value: 36.4952
    - type: nauc_map_at_100_std
      value: 4.9964
    - type: nauc_map_at_100_diff1
      value: 45.5278
    - type: nauc_map_at_1000_max
      value: 36.3394
    - type: nauc_map_at_1000_std
      value: 5.0168
    - type: nauc_map_at_1000_diff1
      value: 45.4435
    - type: nauc_recall_at_1_max
      value: 32.5587
    - type: nauc_recall_at_1_std
      value: -2.3119
    - type: nauc_recall_at_1_diff1
      value: 52.2244
    - type: nauc_recall_at_3_max
      value: 32.2945
    - type: nauc_recall_at_3_std
      value: 3.4591
    - type: nauc_recall_at_3_diff1
      value: 41.0871
    - type: nauc_recall_at_5_max
      value: 29.422500000000003
    - type: nauc_recall_at_5_std
      value: 5.3527
    - type: nauc_recall_at_5_diff1
      value: 36.7172
    - type: nauc_recall_at_10_max
      value: 28.7964
    - type: nauc_recall_at_10_std
      value: 10.3203
    - type: nauc_recall_at_10_diff1
      value: 32.9891
    - type: nauc_recall_at_20_max
      value: 35.9088
    - type: nauc_recall_at_20_std
      value: 17.483999999999998
    - type: nauc_recall_at_20_diff1
      value: 34.1214
    - type: nauc_recall_at_100_max
      value: 40.5066
    - type: nauc_recall_at_100_std
      value: 36.0042
    - type: nauc_recall_at_100_diff1
      value: 25.258999999999997
    - type: nauc_recall_at_1000_max
      value: 68.16980000000001
    - type: nauc_recall_at_1000_std
      value: 78.27300000000001
    - type: nauc_recall_at_1000_diff1
      value: 29.831200000000003
    - type: nauc_precision_at_1_max
      value: 36.5416
    - type: nauc_precision_at_1_std
      value: 1.7398
    - type: nauc_precision_at_1_diff1
      value: 48.6149
    - type: nauc_precision_at_3_max
      value: 34.5475
    - type: nauc_precision_at_3_std
      value: 10.731300000000001
    - type: nauc_precision_at_3_diff1
      value: 26.6094
    - type: nauc_precision_at_5_max
      value: 30.966300000000004
    - type: nauc_precision_at_5_std
      value: 15.614700000000001
    - type: nauc_precision_at_5_diff1
      value: 16.3821
    - type: nauc_precision_at_10_max
      value: 29.3082
    - type: nauc_precision_at_10_std
      value: 22.2006
    - type: nauc_precision_at_10_diff1
      value: 6.5281
    - type: nauc_precision_at_20_max
      value: 23.1867
    - type: nauc_precision_at_20_std
      value: 21.5112
    - type: nauc_precision_at_20_diff1
      value: -2.1949
    - type: nauc_precision_at_100_max
      value: 6.6039
    - type: nauc_precision_at_100_std
      value: 14.7147
    - type: nauc_precision_at_100_diff1
      value: -14.2814
    - type: nauc_precision_at_1000_max
      value: -7.7318
    - type: nauc_precision_at_1000_std
      value: 8.0856
    - type: nauc_precision_at_1000_diff1
      value: -18.8738
    - type: nauc_mrr_at_1_max
      value: 36.5416
    - type: nauc_mrr_at_1_std
      value: 1.7398
    - type: nauc_mrr_at_1_diff1
      value: 48.6149
    - type: nauc_mrr_at_3_max
      value: 37.4645
    - type: nauc_mrr_at_3_std
      value: 4.7265
    - type: nauc_mrr_at_3_diff1
      value: 44.2832
    - type: nauc_mrr_at_5_max
      value: 36.8872
    - type: nauc_mrr_at_5_std
      value: 5.0895
    - type: nauc_mrr_at_5_diff1
      value: 43.1113
    - type: nauc_mrr_at_10_max
      value: 37.1021
    - type: nauc_mrr_at_10_std
      value: 5.7218
    - type: nauc_mrr_at_10_diff1
      value: 43.1786
    - type: nauc_mrr_at_20_max
      value: 37.4827
    - type: nauc_mrr_at_20_std
      value: 5.9467
    - type: nauc_mrr_at_20_diff1
      value: 43.4032
    - type: nauc_mrr_at_100_max
      value: 37.3957
    - type: nauc_mrr_at_100_std
      value: 5.9523
    - type: nauc_mrr_at_100_diff1
      value: 43.3725
    - type: nauc_mrr_at_1000_max
      value: 37.3968
    - type: nauc_mrr_at_1000_std
      value: 5.9475
    - type: nauc_mrr_at_1000_diff1
      value: 43.39
    - type: main_score
      value: 47.301
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CQADupstackWordpressRetrieval (default)
      revision: 4ffe81d471b1924886b33c7567bfb200e9eec5c4
      split: test
      type: mteb/cqadupstack-wordpress
    metrics:
    - type: ndcg_at_1
      value: 25.692999999999998
    - type: ndcg_at_3
      value: 33.0
    - type: ndcg_at_5
      value: 35.736000000000004
    - type: ndcg_at_10
      value: 39.196
    - type: ndcg_at_20
      value: 40.954
    - type: ndcg_at_100
      value: 44.501000000000005
    - type: ndcg_at_1000
      value: 46.482
    - type: map_at_1
      value: 23.851
    - type: map_at_3
      value: 30.270999999999997
    - type: map_at_5
      value: 31.905
    - type: map_at_10
      value: 33.428999999999995
    - type: map_at_20
      value: 33.954
    - type: map_at_100
      value: 34.482
    - type: map_at_1000
      value: 34.57
    - type: recall_at_1
      value: 23.851
    - type: recall_at_3
      value: 38.435
    - type: recall_at_5
      value: 44.872
    - type: recall_at_10
      value: 55.035999999999994
    - type: recall_at_20
      value: 61.529999999999994
    - type: recall_at_100
      value: 79.592
    - type: recall_at_1000
      value: 94.283
    - type: precision_at_1
      value: 25.692999999999998
    - type: precision_at_3
      value: 14.295
    - type: precision_at_5
      value: 10.277
    - type: precision_at_10
      value: 6.433
    - type: precision_at_20
      value: 3.6510000000000002
    - type: precision_at_100
      value: 0.989
    - type: precision_at_1000
      value: 0.128
    - type: mrr_at_1
      value: 25.6932
    - type: mrr_at_3
      value: 32.5323
    - type: mrr_at_5
      value: 34.0203
    - type: mrr_at_10
      value: 35.383199999999995
    - type: mrr_at_20
      value: 35.857499999999995
    - type: mrr_at_100
      value: 36.2947
    - type: mrr_at_1000
      value: 36.3456
    - type: nauc_ndcg_at_1_max
      value: 26.3546
    - type: nauc_ndcg_at_1_std
      value: -7.4308
    - type: nauc_ndcg_at_1_diff1
      value: 50.6893
    - type: nauc_ndcg_at_3_max
      value: 22.5597
    - type: nauc_ndcg_at_3_std
      value: -2.8253
    - type: nauc_ndcg_at_3_diff1
      value: 40.0339
    - type: nauc_ndcg_at_5_max
      value: 23.4927
    - type: nauc_ndcg_at_5_std
      value: -1.8110000000000002
    - type: nauc_ndcg_at_5_diff1
      value: 39.0747
    - type: nauc_ndcg_at_10_max
      value: 22.7233
    - type: nauc_ndcg_at_10_std
      value: -1.2677
    - type: nauc_ndcg_at_10_diff1
      value: 38.4587
    - type: nauc_ndcg_at_20_max
      value: 22.9465
    - type: nauc_ndcg_at_20_std
      value: 0.4223
    - type: nauc_ndcg_at_20_diff1
      value: 38.5424
    - type: nauc_ndcg_at_100_max
      value: 24.7307
    - type: nauc_ndcg_at_100_std
      value: 2.7405
    - type: nauc_ndcg_at_100_diff1
      value: 40.0211
    - type: nauc_ndcg_at_1000_max
      value: 24.7978
    - type: nauc_ndcg_at_1000_std
      value: 1.6664999999999999
    - type: nauc_ndcg_at_1000_diff1
      value: 39.629799999999996
    - type: nauc_map_at_1_max
      value: 23.119
    - type: nauc_map_at_1_std
      value: -8.1386
    - type: nauc_map_at_1_diff1
      value: 50.166999999999994
    - type: nauc_map_at_3_max
      value: 21.9643
    - type: nauc_map_at_3_std
      value: -4.1963
    - type: nauc_map_at_3_diff1
      value: 42.0253
    - type: nauc_map_at_5_max
      value: 23.0779
    - type: nauc_map_at_5_std
      value: -3.4221000000000004
    - type: nauc_map_at_5_diff1
      value: 41.6497
    - type: nauc_map_at_10_max
      value: 23.0936
    - type: nauc_map_at_10_std
      value: -3.107
    - type: nauc_map_at_10_diff1
      value: 41.5032
    - type: nauc_map_at_20_max
      value: 23.2453
    - type: nauc_map_at_20_std
      value: -2.5267999999999997
    - type: nauc_map_at_20_diff1
      value: 41.5085
    - type: nauc_map_at_100_max
      value: 23.552899999999998
    - type: nauc_map_at_100_std
      value: -2.0514
    - type: nauc_map_at_100_diff1
      value: 41.686499999999995
    - type: nauc_map_at_1000_max
      value: 23.5502
    - type: nauc_map_at_1000_std
      value: -2.0632
    - type: nauc_map_at_1000_diff1
      value: 41.634
    - type: nauc_recall_at_1_max
      value: 23.119
    - type: nauc_recall_at_1_std
      value: -8.1386
    - type: nauc_recall_at_1_diff1
      value: 50.166999999999994
    - type: nauc_recall_at_3_max
      value: 19.128700000000002
    - type: nauc_recall_at_3_std
      value: -1.2884
    - type: nauc_recall_at_3_diff1
      value: 33.1893
    - type: nauc_recall_at_5_max
      value: 20.7852
    - type: nauc_recall_at_5_std
      value: 0.9754
    - type: nauc_recall_at_5_diff1
      value: 31.193199999999997
    - type: nauc_recall_at_10_max
      value: 17.5569
    - type: nauc_recall_at_10_std
      value: 2.5935
    - type: nauc_recall_at_10_diff1
      value: 28.5192
    - type: nauc_recall_at_20_max
      value: 17.4543
    - type: nauc_recall_at_20_std
      value: 8.694799999999999
    - type: nauc_recall_at_20_diff1
      value: 28.171200000000002
    - type: nauc_recall_at_100_max
      value: 26.873399999999997
    - type: nauc_recall_at_100_std
      value: 29.0878
    - type: nauc_recall_at_100_diff1
      value: 34.204
    - type: nauc_recall_at_1000_max
      value: 40.9752
    - type: nauc_recall_at_1000_std
      value: 42.8325
    - type: nauc_recall_at_1000_diff1
      value: 20.0664
    - type: nauc_precision_at_1_max
      value: 26.3546
    - type: nauc_precision_at_1_std
      value: -7.4308
    - type: nauc_precision_at_1_diff1
      value: 50.6893
    - type: nauc_precision_at_3_max
      value: 25.078699999999998
    - type: nauc_precision_at_3_std
      value: 3.0139
    - type: nauc_precision_at_3_diff1
      value: 31.566899999999997
    - type: nauc_precision_at_5_max
      value: 29.1348
    - type: nauc_precision_at_5_std
      value: 7.7597
    - type: nauc_precision_at_5_diff1
      value: 26.599899999999998
    - type: nauc_precision_at_10_max
      value: 27.019
    - type: nauc_precision_at_10_std
      value: 11.0219
    - type: nauc_precision_at_10_diff1
      value: 20.9546
    - type: nauc_precision_at_20_max
      value: 27.994200000000003
    - type: nauc_precision_at_20_std
      value: 19.3372
    - type: nauc_precision_at_20_diff1
      value: 17.363400000000002
    - type: nauc_precision_at_100_max
      value: 27.3087
    - type: nauc_precision_at_100_std
      value: 30.3297
    - type: nauc_precision_at_100_diff1
      value: 6.2596
    - type: nauc_precision_at_1000_max
      value: 9.347800000000001
    - type: nauc_precision_at_1000_std
      value: 20.6006
    - type: nauc_precision_at_1000_diff1
      value: -20.9861
    - type: nauc_mrr_at_1_max
      value: 26.3546
    - type: nauc_mrr_at_1_std
      value: -7.4308
    - type: nauc_mrr_at_1_diff1
      value: 50.6893
    - type: nauc_mrr_at_3_max
      value: 25.746799999999997
    - type: nauc_mrr_at_3_std
      value: -2.9107000000000003
    - type: nauc_mrr_at_3_diff1
      value: 43.0073
    - type: nauc_mrr_at_5_max
      value: 25.956400000000002
    - type: nauc_mrr_at_5_std
      value: -2.3782
    - type: nauc_mrr_at_5_diff1
      value: 42.2507
    - type: nauc_mrr_at_10_max
      value: 25.2046
    - type: nauc_mrr_at_10_std
      value: -2.3678999999999997
    - type: nauc_mrr_at_10_diff1
      value: 41.834700000000005
    - type: nauc_mrr_at_20_max
      value: 25.1774
    - type: nauc_mrr_at_20_std
      value: -1.9298
    - type: nauc_mrr_at_20_diff1
      value: 41.8803
    - type: nauc_mrr_at_100_max
      value: 25.4455
    - type: nauc_mrr_at_100_std
      value: -1.6853
    - type: nauc_mrr_at_100_diff1
      value: 42.159
    - type: nauc_mrr_at_1000_max
      value: 25.433899999999998
    - type: nauc_mrr_at_1000_std
      value: -1.7311
    - type: nauc_mrr_at_1000_diff1
      value: 42.159
    - type: main_score
      value: 39.196
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB ClimateFEVER (default)
      revision: 47f2ac6acb640fc46020b02a5b59fdda04d39380
      split: test
      type: mteb/climate-fever
    metrics:
    - type: ndcg_at_1
      value: 32.573
    - type: ndcg_at_3
      value: 27.683000000000003
    - type: ndcg_at_5
      value: 29.537999999999997
    - type: ndcg_at_10
      value: 33.15
    - type: ndcg_at_20
      value: 35.564
    - type: ndcg_at_100
      value: 39.898
    - type: ndcg_at_1000
      value: 43.151
    - type: map_at_1
      value: 14.57
    - type: map_at_3
      value: 20.346
    - type: map_at_5
      value: 22.228
    - type: map_at_10
      value: 24.102
    - type: map_at_20
      value: 24.992
    - type: map_at_100
      value: 25.826
    - type: map_at_1000
      value: 26.021
    - type: recall_at_1
      value: 14.57
    - type: recall_at_3
      value: 25.245
    - type: recall_at_5
      value: 30.820999999999998
    - type: recall_at_10
      value: 38.824999999999996
    - type: recall_at_20
      value: 45.553
    - type: recall_at_100
      value: 62.236999999999995
    - type: recall_at_1000
      value: 80.22
    - type: precision_at_1
      value: 32.573
    - type: precision_at_3
      value: 20.347
    - type: precision_at_5
      value: 15.504999999999999
    - type: precision_at_10
      value: 10.176
    - type: precision_at_20
      value: 6.1339999999999995
    - type: precision_at_100
      value: 1.754
    - type: precision_at_1000
      value: 0.23600000000000002
    - type: mrr_at_1
      value: 32.573299999999996
    - type: mrr_at_3
      value: 41.259499999999996
    - type: mrr_at_5
      value: 43.3116
    - type: mrr_at_10
      value: 44.4113
    - type: mrr_at_20
      value: 44.8728
    - type: mrr_at_100
      value: 45.1757
    - type: mrr_at_1000
      value: 45.2086
    - type: nauc_ndcg_at_1_max
      value: 36.065799999999996
    - type: nauc_ndcg_at_1_std
      value: 17.1124
    - type: nauc_ndcg_at_1_diff1
      value: 27.985
    - type: nauc_ndcg_at_3_max
      value: 36.5467
    - type: nauc_ndcg_at_3_std
      value: 16.403100000000002
    - type: nauc_ndcg_at_3_diff1
      value: 22.1601
    - type: nauc_ndcg_at_5_max
      value: 37.223099999999995
    - type: nauc_ndcg_at_5_std
      value: 18.767300000000002
    - type: nauc_ndcg_at_5_diff1
      value: 20.6143
    - type: nauc_ndcg_at_10_max
      value: 36.8331
    - type: nauc_ndcg_at_10_std
      value: 20.8315
    - type: nauc_ndcg_at_10_diff1
      value: 19.5716
    - type: nauc_ndcg_at_20_max
      value: 36.5592
    - type: nauc_ndcg_at_20_std
      value: 21.4874
    - type: nauc_ndcg_at_20_diff1
      value: 18.4099
    - type: nauc_ndcg_at_100_max
      value: 35.6711
    - type: nauc_ndcg_at_100_std
      value: 22.4637
    - type: nauc_ndcg_at_100_diff1
      value: 18.218500000000002
    - type: nauc_ndcg_at_1000_max
      value: 36.209599999999995
    - type: nauc_ndcg_at_1000_std
      value: 23.3913
    - type: nauc_ndcg_at_1000_diff1
      value: 19.055
    - type: nauc_map_at_1_max
      value: 40.6157
    - type: nauc_map_at_1_std
      value: 13.0776
    - type: nauc_map_at_1_diff1
      value: 30.4958
    - type: nauc_map_at_3_max
      value: 38.3227
    - type: nauc_map_at_3_std
      value: 14.2807
    - type: nauc_map_at_3_diff1
      value: 23.7558
    - type: nauc_map_at_5_max
      value: 37.9312
    - type: nauc_map_at_5_std
      value: 16.206899999999997
    - type: nauc_map_at_5_diff1
      value: 22.4312
    - type: nauc_map_at_10_max
      value: 37.7457
    - type: nauc_map_at_10_std
      value: 17.7945
    - type: nauc_map_at_10_diff1
      value: 21.607000000000003
    - type: nauc_map_at_20_max
      value: 37.727199999999996
    - type: nauc_map_at_20_std
      value: 18.168100000000003
    - type: nauc_map_at_20_diff1
      value: 21.1277
    - type: nauc_map_at_100_max
      value: 37.5139
    - type: nauc_map_at_100_std
      value: 18.4244
    - type: nauc_map_at_100_diff1
      value: 21.082600000000003
    - type: nauc_map_at_1000_max
      value: 37.5088
    - type: nauc_map_at_1000_std
      value: 18.4879
    - type: nauc_map_at_1000_diff1
      value: 21.1075
    - type: nauc_recall_at_1_max
      value: 40.6157
    - type: nauc_recall_at_1_std
      value: 13.0776
    - type: nauc_recall_at_1_diff1
      value: 30.4958
    - type: nauc_recall_at_3_max
      value: 34.0823
    - type: nauc_recall_at_3_std
      value: 14.2898
    - type: nauc_recall_at_3_diff1
      value: 17.8174
    - type: nauc_recall_at_5_max
      value: 33.244099999999996
    - type: nauc_recall_at_5_std
      value: 18.2196
    - type: nauc_recall_at_5_diff1
      value: 14.2718
    - type: nauc_recall_at_10_max
      value: 30.6448
    - type: nauc_recall_at_10_std
      value: 21.323700000000002
    - type: nauc_recall_at_10_diff1
      value: 11.6099
    - type: nauc_recall_at_20_max
      value: 28.523
    - type: nauc_recall_at_20_std
      value: 21.9056
    - type: nauc_recall_at_20_diff1
      value: 8.0707
    - type: nauc_recall_at_100_max
      value: 22.836000000000002
    - type: nauc_recall_at_100_std
      value: 24.8746
    - type: nauc_recall_at_100_diff1
      value: 5.333600000000001
    - type: nauc_recall_at_1000_max
      value: 26.124000000000002
    - type: nauc_recall_at_1000_std
      value: 35.6489
    - type: nauc_recall_at_1000_diff1
      value: 8.5269
    - type: nauc_precision_at_1_max
      value: 36.065799999999996
    - type: nauc_precision_at_1_std
      value: 17.1124
    - type: nauc_precision_at_1_diff1
      value: 27.985
    - type: nauc_precision_at_3_max
      value: 29.9743
    - type: nauc_precision_at_3_std
      value: 19.4935
    - type: nauc_precision_at_3_diff1
      value: 13.7319
    - type: nauc_precision_at_5_max
      value: 26.3111
    - type: nauc_precision_at_5_std
      value: 23.7512
    - type: nauc_precision_at_5_diff1
      value: 8.945699999999999
    - type: nauc_precision_at_10_max
      value: 20.5867
    - type: nauc_precision_at_10_std
      value: 24.1781
    - type: nauc_precision_at_10_diff1
      value: 4.716200000000001
    - type: nauc_precision_at_20_max
      value: 16.9009
    - type: nauc_precision_at_20_std
      value: 23.561799999999998
    - type: nauc_precision_at_20_diff1
      value: 0.26
    - type: nauc_precision_at_100_max
      value: 5.6875
    - type: nauc_precision_at_100_std
      value: 20.5293
    - type: nauc_precision_at_100_diff1
      value: -3.4817
    - type: nauc_precision_at_1000_max
      value: -2.25
    - type: nauc_precision_at_1000_std
      value: 17.2366
    - type: nauc_precision_at_1000_diff1
      value: -4.9703
    - type: nauc_mrr_at_1_max
      value: 36.065799999999996
    - type: nauc_mrr_at_1_std
      value: 17.1124
    - type: nauc_mrr_at_1_diff1
      value: 27.985
    - type: nauc_mrr_at_3_max
      value: 35.9316
    - type: nauc_mrr_at_3_std
      value: 19.3246
    - type: nauc_mrr_at_3_diff1
      value: 23.6033
    - type: nauc_mrr_at_5_max
      value: 36.581
    - type: nauc_mrr_at_5_std
      value: 20.3626
    - type: nauc_mrr_at_5_diff1
      value: 23.1952
    - type: nauc_mrr_at_10_max
      value: 36.5789
    - type: nauc_mrr_at_10_std
      value: 20.6594
    - type: nauc_mrr_at_10_diff1
      value: 23.3078
    - type: nauc_mrr_at_20_max
      value: 36.4621
    - type: nauc_mrr_at_20_std
      value: 20.5731
    - type: nauc_mrr_at_20_diff1
      value: 23.253899999999998
    - type: nauc_mrr_at_100_max
      value: 36.3788
    - type: nauc_mrr_at_100_std
      value: 20.5076
    - type: nauc_mrr_at_100_diff1
      value: 23.1904
    - type: nauc_mrr_at_1000_max
      value: 36.383500000000005
    - type: nauc_mrr_at_1000_std
      value: 20.505399999999998
    - type: nauc_mrr_at_1000_diff1
      value: 23.2106
    - type: main_score
      value: 33.15
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CodeFeedbackMT (default)
      revision: b0f12fa0c0dd67f59c95a5c33d02aeeb4c398c5f
      split: test
      type: CoIR-Retrieval/codefeedback-mt
    metrics:
    - type: ndcg_at_1
      value: 30.270000000000003
    - type: ndcg_at_3
      value: 37.797
    - type: ndcg_at_5
      value: 40.147
    - type: ndcg_at_10
      value: 42.136
    - type: ndcg_at_20
      value: 43.655
    - type: ndcg_at_100
      value: 45.95
    - type: ndcg_at_1000
      value: 47.510999999999996
    - type: map_at_1
      value: 30.270000000000003
    - type: map_at_3
      value: 35.949
    - type: map_at_5
      value: 37.254
    - type: map_at_10
      value: 38.076
    - type: map_at_20
      value: 38.492
    - type: map_at_100
      value: 38.805
    - type: map_at_1000
      value: 38.858
    - type: recall_at_1
      value: 30.270000000000003
    - type: recall_at_3
      value: 43.142
    - type: recall_at_5
      value: 48.844
    - type: recall_at_10
      value: 54.99000000000001
    - type: recall_at_20
      value: 61.007999999999996
    - type: recall_at_100
      value: 73.443
    - type: recall_at_1000
      value: 86.066
    - type: precision_at_1
      value: 30.270000000000003
    - type: precision_at_3
      value: 14.381
    - type: precision_at_5
      value: 9.769
    - type: precision_at_10
      value: 5.499
    - type: precision_at_20
      value: 3.05
    - type: precision_at_100
      value: 0.734
    - type: precision_at_1000
      value: 0.086
    - type: mrr_at_1
      value: 30.2704
    - type: mrr_at_3
      value: 35.9494
    - type: mrr_at_5
      value: 37.2539
    - type: mrr_at_10
      value: 38.0763
    - type: mrr_at_20
      value: 38.4916
    - type: mrr_at_100
      value: 38.8047
    - type: mrr_at_1000
      value: 38.8578
    - type: nauc_ndcg_at_1_max
      value: 13.1327
    - type: nauc_ndcg_at_1_std
      value: -20.450599999999998
    - type: nauc_ndcg_at_1_diff1
      value: 53.905800000000006
    - type: nauc_ndcg_at_3_max
      value: 15.181000000000001
    - type: nauc_ndcg_at_3_std
      value: -20.877399999999998
    - type: nauc_ndcg_at_3_diff1
      value: 49.1269
    - type: nauc_ndcg_at_5_max
      value: 15.7972
    - type: nauc_ndcg_at_5_std
      value: -20.6361
    - type: nauc_ndcg_at_5_diff1
      value: 47.826800000000006
    - type: nauc_ndcg_at_10_max
      value: 16.4268
    - type: nauc_ndcg_at_10_std
      value: -20.0384
    - type: nauc_ndcg_at_10_diff1
      value: 47.0914
    - type: nauc_ndcg_at_20_max
      value: 17.1004
    - type: nauc_ndcg_at_20_std
      value: -18.9344
    - type: nauc_ndcg_at_20_diff1
      value: 46.6149
    - type: nauc_ndcg_at_100_max
      value: 17.6904
    - type: nauc_ndcg_at_100_std
      value: -17.1856
    - type: nauc_ndcg_at_100_diff1
      value: 46.3637
    - type: nauc_ndcg_at_1000_max
      value: 17.5049
    - type: nauc_ndcg_at_1000_std
      value: -16.7834
    - type: nauc_ndcg_at_1000_diff1
      value: 46.5672
    - type: nauc_map_at_1_max
      value: 13.1327
    - type: nauc_map_at_1_std
      value: -20.450599999999998
    - type: nauc_map_at_1_diff1
      value: 53.905800000000006
    - type: nauc_map_at_3_max
      value: 14.723500000000001
    - type: nauc_map_at_3_std
      value: -20.7922
    - type: nauc_map_at_3_diff1
      value: 50.275000000000006
    - type: nauc_map_at_5_max
      value: 15.061399999999999
    - type: nauc_map_at_5_std
      value: -20.6704
    - type: nauc_map_at_5_diff1
      value: 49.5612
    - type: nauc_map_at_10_max
      value: 15.292900000000001
    - type: nauc_map_at_10_std
      value: -20.4431
    - type: nauc_map_at_10_diff1
      value: 49.2676
    - type: nauc_map_at_20_max
      value: 15.4694
    - type: nauc_map_at_20_std
      value: -20.1497
    - type: nauc_map_at_20_diff1
      value: 49.1538
    - type: nauc_map_at_100_max
      value: 15.5383
    - type: nauc_map_at_100_std
      value: -19.9266
    - type: nauc_map_at_100_diff1
      value: 49.1303
    - type: nauc_map_at_1000_max
      value: 15.5348
    - type: nauc_map_at_1000_std
      value: -19.9076
    - type: nauc_map_at_1000_diff1
      value: 49.138799999999996
    - type: nauc_recall_at_1_max
      value: 13.1327
    - type: nauc_recall_at_1_std
      value: -20.450599999999998
    - type: nauc_recall_at_1_diff1
      value: 53.905800000000006
    - type: nauc_recall_at_3_max
      value: 16.467599999999997
    - type: nauc_recall_at_3_std
      value: -21.1125
    - type: nauc_recall_at_3_diff1
      value: 45.8636
    - type: nauc_recall_at_5_max
      value: 17.996699999999997
    - type: nauc_recall_at_5_std
      value: -20.4801
    - type: nauc_recall_at_5_diff1
      value: 42.6329
    - type: nauc_recall_at_10_max
      value: 20.258100000000002
    - type: nauc_recall_at_10_std
      value: -18.4556
    - type: nauc_recall_at_10_diff1
      value: 39.9989
    - type: nauc_recall_at_20_max
      value: 23.4684
    - type: nauc_recall_at_20_std
      value: -13.5326
    - type: nauc_recall_at_20_diff1
      value: 37.3551
    - type: nauc_recall_at_100_max
      value: 29.868499999999997
    - type: nauc_recall_at_100_std
      value: 1.2361
    - type: nauc_recall_at_100_diff1
      value: 32.6178
    - type: nauc_recall_at_1000_max
      value: 34.7721
    - type: nauc_recall_at_1000_std
      value: 21.076700000000002
    - type: nauc_recall_at_1000_diff1
      value: 26.4002
    - type: nauc_precision_at_1_max
      value: 13.1327
    - type: nauc_precision_at_1_std
      value: -20.450599999999998
    - type: nauc_precision_at_1_diff1
      value: 53.905800000000006
    - type: nauc_precision_at_3_max
      value: 16.467599999999997
    - type: nauc_precision_at_3_std
      value: -21.1125
    - type: nauc_precision_at_3_diff1
      value: 45.8636
    - type: nauc_precision_at_5_max
      value: 17.996699999999997
    - type: nauc_precision_at_5_std
      value: -20.4801
    - type: nauc_precision_at_5_diff1
      value: 42.6329
    - type: nauc_precision_at_10_max
      value: 20.258100000000002
    - type: nauc_precision_at_10_std
      value: -18.4556
    - type: nauc_precision_at_10_diff1
      value: 39.9989
    - type: nauc_precision_at_20_max
      value: 23.4684
    - type: nauc_precision_at_20_std
      value: -13.5326
    - type: nauc_precision_at_20_diff1
      value: 37.3551
    - type: nauc_precision_at_100_max
      value: 29.868499999999997
    - type: nauc_precision_at_100_std
      value: 1.2361
    - type: nauc_precision_at_100_diff1
      value: 32.6178
    - type: nauc_precision_at_1000_max
      value: 34.7721
    - type: nauc_precision_at_1000_std
      value: 21.076700000000002
    - type: nauc_precision_at_1000_diff1
      value: 26.4002
    - type: nauc_mrr_at_1_max
      value: 13.1327
    - type: nauc_mrr_at_1_std
      value: -20.450599999999998
    - type: nauc_mrr_at_1_diff1
      value: 53.905800000000006
    - type: nauc_mrr_at_3_max
      value: 14.723500000000001
    - type: nauc_mrr_at_3_std
      value: -20.7922
    - type: nauc_mrr_at_3_diff1
      value: 50.275000000000006
    - type: nauc_mrr_at_5_max
      value: 15.061399999999999
    - type: nauc_mrr_at_5_std
      value: -20.6704
    - type: nauc_mrr_at_5_diff1
      value: 49.5612
    - type: nauc_mrr_at_10_max
      value: 15.292900000000001
    - type: nauc_mrr_at_10_std
      value: -20.4431
    - type: nauc_mrr_at_10_diff1
      value: 49.2676
    - type: nauc_mrr_at_20_max
      value: 15.4694
    - type: nauc_mrr_at_20_std
      value: -20.1497
    - type: nauc_mrr_at_20_diff1
      value: 49.1538
    - type: nauc_mrr_at_100_max
      value: 15.5383
    - type: nauc_mrr_at_100_std
      value: -19.9266
    - type: nauc_mrr_at_100_diff1
      value: 49.1303
    - type: nauc_mrr_at_1000_max
      value: 15.5348
    - type: nauc_mrr_at_1000_std
      value: -19.9076
    - type: nauc_mrr_at_1000_diff1
      value: 49.138799999999996
    - type: main_score
      value: 42.136
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CodeFeedbackST (default)
      revision: d213819e87aab9010628da8b73ab4eb337c89340
      split: test
      type: CoIR-Retrieval/codefeedback-st
    metrics:
    - type: ndcg_at_1
      value: 59.621
    - type: ndcg_at_3
      value: 71.255
    - type: ndcg_at_5
      value: 73.71
    - type: ndcg_at_10
      value: 75.276
    - type: ndcg_at_20
      value: 76.115
    - type: ndcg_at_100
      value: 76.91900000000001
    - type: ndcg_at_1000
      value: 77.172
    - type: map_at_1
      value: 59.621
    - type: map_at_3
      value: 68.449
    - type: map_at_5
      value: 69.817
    - type: map_at_10
      value: 70.474
    - type: map_at_20
      value: 70.707
    - type: map_at_100
      value: 70.82300000000001
    - type: map_at_1000
      value: 70.833
    - type: recall_at_1
      value: 59.621
    - type: recall_at_3
      value: 79.352
    - type: recall_at_5
      value: 85.28999999999999
    - type: recall_at_10
      value: 90.079
    - type: recall_at_20
      value: 93.372
    - type: recall_at_100
      value: 97.649
    - type: recall_at_1000
      value: 99.604
    - type: precision_at_1
      value: 59.621
    - type: precision_at_3
      value: 26.451
    - type: precision_at_5
      value: 17.058
    - type: precision_at_10
      value: 9.008
    - type: precision_at_20
      value: 4.6690000000000005
    - type: precision_at_100
      value: 0.976
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 59.5796
    - type: mrr_at_3
      value: 68.42190000000001
    - type: mrr_at_5
      value: 69.8065
    - type: mrr_at_10
      value: 70.4563
    - type: mrr_at_20
      value: 70.69
    - type: mrr_at_100
      value: 70.80539999999999
    - type: mrr_at_1000
      value: 70.8155
    - type: nauc_ndcg_at_1_max
      value: 1.0058
    - type: nauc_ndcg_at_1_std
      value: -28.633999999999997
    - type: nauc_ndcg_at_1_diff1
      value: 74.2731
    - type: nauc_ndcg_at_3_max
      value: 5.9328
    - type: nauc_ndcg_at_3_std
      value: -33.4034
    - type: nauc_ndcg_at_3_diff1
      value: 69.0612
    - type: nauc_ndcg_at_5_max
      value: 6.3485
    - type: nauc_ndcg_at_5_std
      value: -33.4167
    - type: nauc_ndcg_at_5_diff1
      value: 68.9449
    - type: nauc_ndcg_at_10_max
      value: 6.0459
    - type: nauc_ndcg_at_10_std
      value: -32.6233
    - type: nauc_ndcg_at_10_diff1
      value: 69.0512
    - type: nauc_ndcg_at_20_max
      value: 5.8008
    - type: nauc_ndcg_at_20_std
      value: -32.0714
    - type: nauc_ndcg_at_20_diff1
      value: 69.5449
    - type: nauc_ndcg_at_100_max
      value: 5.5014
    - type: nauc_ndcg_at_100_std
      value: -31.5492
    - type: nauc_ndcg_at_100_diff1
      value: 69.9543
    - type: nauc_ndcg_at_1000_max
      value: 5.2358
    - type: nauc_ndcg_at_1000_std
      value: -31.638899999999996
    - type: nauc_ndcg_at_1000_diff1
      value: 70.0955
    - type: nauc_map_at_1_max
      value: 1.0058
    - type: nauc_map_at_1_std
      value: -28.633999999999997
    - type: nauc_map_at_1_diff1
      value: 74.2731
    - type: nauc_map_at_3_max
      value: 4.5532
    - type: nauc_map_at_3_std
      value: -32.0989
    - type: nauc_map_at_3_diff1
      value: 70.47879999999999
    - type: nauc_map_at_5_max
      value: 4.7025
    - type: nauc_map_at_5_std
      value: -32.0494
    - type: nauc_map_at_5_diff1
      value: 70.4832
    - type: nauc_map_at_10_max
      value: 4.5632
    - type: nauc_map_at_10_std
      value: -31.750899999999998
    - type: nauc_map_at_10_diff1
      value: 70.556
    - type: nauc_map_at_20_max
      value: 4.4907
    - type: nauc_map_at_20_std
      value: -31.6179
    - type: nauc_map_at_20_diff1
      value: 70.6865
    - type: nauc_map_at_100_max
      value: 4.4536
    - type: nauc_map_at_100_std
      value: -31.5575
    - type: nauc_map_at_100_diff1
      value: 70.7379
    - type: nauc_map_at_1000_max
      value: 4.4467
    - type: nauc_map_at_1000_std
      value: -31.557000000000002
    - type: nauc_map_at_1000_diff1
      value: 70.7424
    - type: nauc_recall_at_1_max
      value: 1.0058
    - type: nauc_recall_at_1_std
      value: -28.633999999999997
    - type: nauc_recall_at_1_diff1
      value: 74.2731
    - type: nauc_recall_at_3_max
      value: 11.3291
    - type: nauc_recall_at_3_std
      value: -38.4878
    - type: nauc_recall_at_3_diff1
      value: 63.5405
    - type: nauc_recall_at_5_max
      value: 14.802499999999998
    - type: nauc_recall_at_5_std
      value: -40.3304
    - type: nauc_recall_at_5_diff1
      value: 61.142300000000006
    - type: nauc_recall_at_10_max
      value: 16.3095
    - type: nauc_recall_at_10_std
      value: -37.9007
    - type: nauc_recall_at_10_diff1
      value: 58.5604
    - type: nauc_recall_at_20_max
      value: 18.5464
    - type: nauc_recall_at_20_std
      value: -33.8926
    - type: nauc_recall_at_20_diff1
      value: 59.15709999999999
    - type: nauc_recall_at_100_max
      value: 28.231499999999997
    - type: nauc_recall_at_100_std
      value: -14.0739
    - type: nauc_recall_at_100_diff1
      value: 58.1862
    - type: nauc_recall_at_1000_max
      value: 35.3579
    - type: nauc_recall_at_1000_std
      value: 27.673
    - type: nauc_recall_at_1000_diff1
      value: 53.6523
    - type: nauc_precision_at_1_max
      value: 1.0058
    - type: nauc_precision_at_1_std
      value: -28.633999999999997
    - type: nauc_precision_at_1_diff1
      value: 74.2731
    - type: nauc_precision_at_3_max
      value: 11.3291
    - type: nauc_precision_at_3_std
      value: -38.4878
    - type: nauc_precision_at_3_diff1
      value: 63.5405
    - type: nauc_precision_at_5_max
      value: 14.802499999999998
    - type: nauc_precision_at_5_std
      value: -40.3304
    - type: nauc_precision_at_5_diff1
      value: 61.142300000000006
    - type: nauc_precision_at_10_max
      value: 16.3095
    - type: nauc_precision_at_10_std
      value: -37.9007
    - type: nauc_precision_at_10_diff1
      value: 58.5604
    - type: nauc_precision_at_20_max
      value: 18.5464
    - type: nauc_precision_at_20_std
      value: -33.8926
    - type: nauc_precision_at_20_diff1
      value: 59.15709999999999
    - type: nauc_precision_at_100_max
      value: 28.231499999999997
    - type: nauc_precision_at_100_std
      value: -14.0739
    - type: nauc_precision_at_100_diff1
      value: 58.1862
    - type: nauc_precision_at_1000_max
      value: 35.3579
    - type: nauc_precision_at_1000_std
      value: 27.673
    - type: nauc_precision_at_1000_diff1
      value: 53.6523
    - type: nauc_mrr_at_1_max
      value: 0.4596
    - type: nauc_mrr_at_1_std
      value: -28.4399
    - type: nauc_mrr_at_1_diff1
      value: 74.32849999999999
    - type: nauc_mrr_at_3_max
      value: 4.2199
    - type: nauc_mrr_at_3_std
      value: -31.9909
    - type: nauc_mrr_at_3_diff1
      value: 70.5363
    - type: nauc_mrr_at_5_max
      value: 4.3676
    - type: nauc_mrr_at_5_std
      value: -31.947599999999998
    - type: nauc_mrr_at_5_diff1
      value: 70.5144
    - type: nauc_mrr_at_10_max
      value: 4.2149
    - type: nauc_mrr_at_10_std
      value: -31.647
    - type: nauc_mrr_at_10_diff1
      value: 70.598
    - type: nauc_mrr_at_20_max
      value: 4.1426
    - type: nauc_mrr_at_20_std
      value: -31.513799999999996
    - type: nauc_mrr_at_20_diff1
      value: 70.729
    - type: nauc_mrr_at_100_max
      value: 4.104
    - type: nauc_mrr_at_100_std
      value: -31.451800000000002
    - type: nauc_mrr_at_100_diff1
      value: 70.7809
    - type: nauc_mrr_at_1000_max
      value: 4.0969999999999995
    - type: nauc_mrr_at_1000_std
      value: -31.4513
    - type: nauc_mrr_at_1000_diff1
      value: 70.78529999999999
    - type: main_score
      value: 75.276
    task:
      type: Retrieval
  - dataset:
      config: python
      name: MTEB CodeSearchNetCCRetrieval (python)
      revision: 6e1effa2c03723c5fde48ee912b5ee08d4f211e8
      split: test
      type: CoIR-Retrieval/CodeSearchNet-ccr
    metrics:
    - type: ndcg_at_1
      value: 36.955
    - type: ndcg_at_3
      value: 46.436
    - type: ndcg_at_5
      value: 49.055
    - type: ndcg_at_10
      value: 51.408
    - type: ndcg_at_20
      value: 52.93600000000001
    - type: ndcg_at_100
      value: 55.089999999999996
    - type: ndcg_at_1000
      value: 56.406
    - type: map_at_1
      value: 36.955
    - type: map_at_3
      value: 44.112
    - type: map_at_5
      value: 45.565
    - type: map_at_10
      value: 46.538000000000004
    - type: map_at_20
      value: 46.958
    - type: map_at_100
      value: 47.253
    - type: map_at_1000
      value: 47.298
    - type: recall_at_1
      value: 36.955
    - type: recall_at_3
      value: 53.157
    - type: recall_at_5
      value: 59.519
    - type: recall_at_10
      value: 66.78500000000001
    - type: recall_at_20
      value: 72.82499999999999
    - type: recall_at_100
      value: 84.482
    - type: recall_at_1000
      value: 95.06599999999999
    - type: precision_at_1
      value: 36.955
    - type: precision_at_3
      value: 17.718999999999998
    - type: precision_at_5
      value: 11.904
    - type: precision_at_10
      value: 6.679
    - type: precision_at_20
      value: 3.641
    - type: precision_at_100
      value: 0.845
    - type: precision_at_1000
      value: 0.095
    - type: mrr_at_1
      value: 36.9487
    - type: mrr_at_3
      value: 44.1044
    - type: mrr_at_5
      value: 45.556999999999995
    - type: mrr_at_10
      value: 46.531
    - type: mrr_at_20
      value: 46.9517
    - type: mrr_at_100
      value: 47.246300000000005
    - type: mrr_at_1000
      value: 47.2918
    - type: nauc_ndcg_at_1_max
      value: 30.887500000000003
    - type: nauc_ndcg_at_1_std
      value: -5.4391
    - type: nauc_ndcg_at_1_diff1
      value: 53.215199999999996
    - type: nauc_ndcg_at_3_max
      value: 31.4697
    - type: nauc_ndcg_at_3_std
      value: -5.3775
    - type: nauc_ndcg_at_3_diff1
      value: 48.6991
    - type: nauc_ndcg_at_5_max
      value: 31.4647
    - type: nauc_ndcg_at_5_std
      value: -5.022
    - type: nauc_ndcg_at_5_diff1
      value: 48.0297
    - type: nauc_ndcg_at_10_max
      value: 31.5139
    - type: nauc_ndcg_at_10_std
      value: -4.3081000000000005
    - type: nauc_ndcg_at_10_diff1
      value: 47.6012
    - type: nauc_ndcg_at_20_max
      value: 31.4083
    - type: nauc_ndcg_at_20_std
      value: -3.7769999999999997
    - type: nauc_ndcg_at_20_diff1
      value: 47.4673
    - type: nauc_ndcg_at_100_max
      value: 31.432100000000002
    - type: nauc_ndcg_at_100_std
      value: -3.3629
    - type: nauc_ndcg_at_100_diff1
      value: 47.5608
    - type: nauc_ndcg_at_1000_max
      value: 31.521500000000003
    - type: nauc_ndcg_at_1000_std
      value: -3.4922
    - type: nauc_ndcg_at_1000_diff1
      value: 47.997299999999996
    - type: nauc_map_at_1_max
      value: 30.887500000000003
    - type: nauc_map_at_1_std
      value: -5.4391
    - type: nauc_map_at_1_diff1
      value: 53.215199999999996
    - type: nauc_map_at_3_max
      value: 31.3321
    - type: nauc_map_at_3_std
      value: -5.3912
    - type: nauc_map_at_3_diff1
      value: 49.7525
    - type: nauc_map_at_5_max
      value: 31.324600000000004
    - type: nauc_map_at_5_std
      value: -5.197100000000001
    - type: nauc_map_at_5_diff1
      value: 49.4028
    - type: nauc_map_at_10_max
      value: 31.3398
    - type: nauc_map_at_10_std
      value: -4.9248
    - type: nauc_map_at_10_diff1
      value: 49.2583
    - type: nauc_map_at_20_max
      value: 31.309199999999997
    - type: nauc_map_at_20_std
      value: -4.7903
    - type: nauc_map_at_20_diff1
      value: 49.2312
    - type: nauc_map_at_100_max
      value: 31.305
    - type: nauc_map_at_100_std
      value: -4.7492
    - type: nauc_map_at_100_diff1
      value: 49.2452
    - type: nauc_map_at_1000_max
      value: 31.3077
    - type: nauc_map_at_1000_std
      value: -4.7505
    - type: nauc_map_at_1000_diff1
      value: 49.2596
    - type: nauc_recall_at_1_max
      value: 30.887500000000003
    - type: nauc_recall_at_1_std
      value: -5.4391
    - type: nauc_recall_at_1_diff1
      value: 53.215199999999996
    - type: nauc_recall_at_3_max
      value: 31.877899999999997
    - type: nauc_recall_at_3_std
      value: -5.3372
    - type: nauc_recall_at_3_diff1
      value: 45.5796
    - type: nauc_recall_at_5_max
      value: 31.9064
    - type: nauc_recall_at_5_std
      value: -4.4158
    - type: nauc_recall_at_5_diff1
      value: 43.6238
    - type: nauc_recall_at_10_max
      value: 32.1625
    - type: nauc_recall_at_10_std
      value: -1.6879000000000002
    - type: nauc_recall_at_10_diff1
      value: 41.4155
    - type: nauc_recall_at_20_max
      value: 31.7318
    - type: nauc_recall_at_20_std
      value: 1.4794
    - type: nauc_recall_at_20_diff1
      value: 39.7822
    - type: nauc_recall_at_100_max
      value: 32.399899999999995
    - type: nauc_recall_at_100_std
      value: 9.331299999999999
    - type: nauc_recall_at_100_diff1
      value: 36.4089
    - type: nauc_recall_at_1000_max
      value: 38.488299999999995
    - type: nauc_recall_at_1000_std
      value: 26.7544
    - type: nauc_recall_at_1000_diff1
      value: 34.8223
    - type: nauc_precision_at_1_max
      value: 30.887500000000003
    - type: nauc_precision_at_1_std
      value: -5.4391
    - type: nauc_precision_at_1_diff1
      value: 53.215199999999996
    - type: nauc_precision_at_3_max
      value: 31.877899999999997
    - type: nauc_precision_at_3_std
      value: -5.3372
    - type: nauc_precision_at_3_diff1
      value: 45.5796
    - type: nauc_precision_at_5_max
      value: 31.9064
    - type: nauc_precision_at_5_std
      value: -4.4158
    - type: nauc_precision_at_5_diff1
      value: 43.6238
    - type: nauc_precision_at_10_max
      value: 32.1625
    - type: nauc_precision_at_10_std
      value: -1.6879000000000002
    - type: nauc_precision_at_10_diff1
      value: 41.4155
    - type: nauc_precision_at_20_max
      value: 31.7318
    - type: nauc_precision_at_20_std
      value: 1.4794
    - type: nauc_precision_at_20_diff1
      value: 39.7822
    - type: nauc_precision_at_100_max
      value: 32.399899999999995
    - type: nauc_precision_at_100_std
      value: 9.331299999999999
    - type: nauc_precision_at_100_diff1
      value: 36.4089
    - type: nauc_precision_at_1000_max
      value: 38.488299999999995
    - type: nauc_precision_at_1000_std
      value: 26.7544
    - type: nauc_precision_at_1000_diff1
      value: 34.8223
    - type: nauc_mrr_at_1_max
      value: 30.950899999999997
    - type: nauc_mrr_at_1_std
      value: -5.4719
    - type: nauc_mrr_at_1_diff1
      value: 53.235699999999994
    - type: nauc_mrr_at_3_max
      value: 31.374000000000002
    - type: nauc_mrr_at_3_std
      value: -5.4241
    - type: nauc_mrr_at_3_diff1
      value: 49.7741
    - type: nauc_mrr_at_5_max
      value: 31.3677
    - type: nauc_mrr_at_5_std
      value: -5.2233
    - type: nauc_mrr_at_5_diff1
      value: 49.4223
    - type: nauc_mrr_at_10_max
      value: 31.3811
    - type: nauc_mrr_at_10_std
      value: -4.952100000000001
    - type: nauc_mrr_at_10_diff1
      value: 49.2782
    - type: nauc_mrr_at_20_max
      value: 31.3498
    - type: nauc_mrr_at_20_std
      value: -4.8186
    - type: nauc_mrr_at_20_diff1
      value: 49.2501
    - type: nauc_mrr_at_100_max
      value: 31.3459
    - type: nauc_mrr_at_100_std
      value: -4.7777
    - type: nauc_mrr_at_100_diff1
      value: 49.2643
    - type: nauc_mrr_at_1000_max
      value: 31.3487
    - type: nauc_mrr_at_1000_std
      value: -4.779
    - type: nauc_mrr_at_1000_diff1
      value: 49.2787
    - type: main_score
      value: 51.408
    task:
      type: Retrieval
  - dataset:
      config: javascript
      name: MTEB CodeSearchNetCCRetrieval (javascript)
      revision: 6e1effa2c03723c5fde48ee912b5ee08d4f211e8
      split: test
      type: CoIR-Retrieval/CodeSearchNet-ccr
    metrics:
    - type: ndcg_at_1
      value: 38.833
    - type: ndcg_at_3
      value: 47.698
    - type: ndcg_at_5
      value: 49.964999999999996
    - type: ndcg_at_10
      value: 52.035
    - type: ndcg_at_20
      value: 53.49
    - type: ndcg_at_100
      value: 55.696999999999996
    - type: ndcg_at_1000
      value: 57.037000000000006
    - type: map_at_1
      value: 38.833
    - type: map_at_3
      value: 45.559
    - type: map_at_5
      value: 46.817
    - type: map_at_10
      value: 47.675
    - type: map_at_20
      value: 48.079
    - type: map_at_100
      value: 48.375
    - type: map_at_1000
      value: 48.42
    - type: recall_at_1
      value: 38.833
    - type: recall_at_3
      value: 53.874
    - type: recall_at_5
      value: 59.374
    - type: recall_at_10
      value: 65.755
    - type: recall_at_20
      value: 71.468
    - type: recall_at_100
      value: 83.5
    - type: recall_at_1000
      value: 94.348
    - type: precision_at_1
      value: 38.833
    - type: precision_at_3
      value: 17.958
    - type: precision_at_5
      value: 11.875
    - type: precision_at_10
      value: 6.576
    - type: precision_at_20
      value: 3.573
    - type: precision_at_100
      value: 0.835
    - type: precision_at_1000
      value: 0.094
    - type: mrr_at_1
      value: 38.8332
    - type: mrr_at_3
      value: 45.5485
    - type: mrr_at_5
      value: 46.814
    - type: mrr_at_10
      value: 47.6716
    - type: mrr_at_20
      value: 48.0761
    - type: mrr_at_100
      value: 48.3716
    - type: mrr_at_1000
      value: 48.4167
    - type: nauc_ndcg_at_1_max
      value: 26.1449
    - type: nauc_ndcg_at_1_std
      value: -10.991299999999999
    - type: nauc_ndcg_at_1_diff1
      value: 55.970299999999995
    - type: nauc_ndcg_at_3_max
      value: 29.7447
    - type: nauc_ndcg_at_3_std
      value: -9.610299999999999
    - type: nauc_ndcg_at_3_diff1
      value: 52.031499999999994
    - type: nauc_ndcg_at_5_max
      value: 29.1562
    - type: nauc_ndcg_at_5_std
      value: -9.288499999999999
    - type: nauc_ndcg_at_5_diff1
      value: 50.8454
    - type: nauc_ndcg_at_10_max
      value: 28.1795
    - type: nauc_ndcg_at_10_std
      value: -9.5992
    - type: nauc_ndcg_at_10_diff1
      value: 50.6937
    - type: nauc_ndcg_at_20_max
      value: 27.8613
    - type: nauc_ndcg_at_20_std
      value: -9.425500000000001
    - type: nauc_ndcg_at_20_diff1
      value: 50.5688
    - type: nauc_ndcg_at_100_max
      value: 27.9792
    - type: nauc_ndcg_at_100_std
      value: -8.792300000000001
    - type: nauc_ndcg_at_100_diff1
      value: 50.868500000000004
    - type: nauc_ndcg_at_1000_max
      value: 28.0666
    - type: nauc_ndcg_at_1000_std
      value: -8.928899999999999
    - type: nauc_ndcg_at_1000_diff1
      value: 51.1663
    - type: nauc_map_at_1_max
      value: 26.1449
    - type: nauc_map_at_1_std
      value: -10.991299999999999
    - type: nauc_map_at_1_diff1
      value: 55.970299999999995
    - type: nauc_map_at_3_max
      value: 28.921799999999998
    - type: nauc_map_at_3_std
      value: -9.9782
    - type: nauc_map_at_3_diff1
      value: 52.965700000000005
    - type: nauc_map_at_5_max
      value: 28.575899999999997
    - type: nauc_map_at_5_std
      value: -9.822799999999999
    - type: nauc_map_at_5_diff1
      value: 52.32790000000001
    - type: nauc_map_at_10_max
      value: 28.1738
    - type: nauc_map_at_10_std
      value: -9.933300000000001
    - type: nauc_map_at_10_diff1
      value: 52.26690000000001
    - type: nauc_map_at_20_max
      value: 28.0844
    - type: nauc_map_at_20_std
      value: -9.8925
    - type: nauc_map_at_20_diff1
      value: 52.2407
    - type: nauc_map_at_100_max
      value: 28.0938
    - type: nauc_map_at_100_std
      value: -9.8258
    - type: nauc_map_at_100_diff1
      value: 52.2776
    - type: nauc_map_at_1000_max
      value: 28.092299999999998
    - type: nauc_map_at_1000_std
      value: -9.832
    - type: nauc_map_at_1000_diff1
      value: 52.2874
    - type: nauc_recall_at_1_max
      value: 26.1449
    - type: nauc_recall_at_1_std
      value: -10.991299999999999
    - type: nauc_recall_at_1_diff1
      value: 55.970299999999995
    - type: nauc_recall_at_3_max
      value: 32.1929
    - type: nauc_recall_at_3_std
      value: -8.491200000000001
    - type: nauc_recall_at_3_diff1
      value: 49.2364
    - type: nauc_recall_at_5_max
      value: 30.8852
    - type: nauc_recall_at_5_std
      value: -7.518700000000001
    - type: nauc_recall_at_5_diff1
      value: 46.004400000000004
    - type: nauc_recall_at_10_max
      value: 27.6397
    - type: nauc_recall_at_10_std
      value: -8.5506
    - type: nauc_recall_at_10_diff1
      value: 45.012299999999996
    - type: nauc_recall_at_20_max
      value: 26.026300000000003
    - type: nauc_recall_at_20_std
      value: -7.5049
    - type: nauc_recall_at_20_diff1
      value: 43.6556
    - type: nauc_recall_at_100_max
      value: 26.3742
    - type: nauc_recall_at_100_std
      value: 0.46940000000000004
    - type: nauc_recall_at_100_diff1
      value: 43.1361
    - type: nauc_recall_at_1000_max
      value: 28.3536
    - type: nauc_recall_at_1000_std
      value: 11.2799
    - type: nauc_recall_at_1000_diff1
      value: 41.8369
    - type: nauc_precision_at_1_max
      value: 26.1449
    - type: nauc_precision_at_1_std
      value: -10.991299999999999
    - type: nauc_precision_at_1_diff1
      value: 55.970299999999995
    - type: nauc_precision_at_3_max
      value: 32.1929
    - type: nauc_precision_at_3_std
      value: -8.491200000000001
    - type: nauc_precision_at_3_diff1
      value: 49.2364
    - type: nauc_precision_at_5_max
      value: 30.8852
    - type: nauc_precision_at_5_std
      value: -7.518700000000001
    - type: nauc_precision_at_5_diff1
      value: 46.004400000000004
    - type: nauc_precision_at_10_max
      value: 27.6397
    - type: nauc_precision_at_10_std
      value: -8.5506
    - type: nauc_precision_at_10_diff1
      value: 45.012299999999996
    - type: nauc_precision_at_20_max
      value: 26.026300000000003
    - type: nauc_precision_at_20_std
      value: -7.5049
    - type: nauc_precision_at_20_diff1
      value: 43.6556
    - type: nauc_precision_at_100_max
      value: 26.3742
    - type: nauc_precision_at_100_std
      value: 0.46940000000000004
    - type: nauc_precision_at_100_diff1
      value: 43.1361
    - type: nauc_precision_at_1000_max
      value: 28.3536
    - type: nauc_precision_at_1000_std
      value: 11.2799
    - type: nauc_precision_at_1000_diff1
      value: 41.8369
    - type: nauc_mrr_at_1_max
      value: 26.1449
    - type: nauc_mrr_at_1_std
      value: -10.991299999999999
    - type: nauc_mrr_at_1_diff1
      value: 55.970299999999995
    - type: nauc_mrr_at_3_max
      value: 28.9026
    - type: nauc_mrr_at_3_std
      value: -10.0274
    - type: nauc_mrr_at_3_diff1
      value: 52.9705
    - type: nauc_mrr_at_5_max
      value: 28.571
    - type: nauc_mrr_at_5_std
      value: -9.8353
    - type: nauc_mrr_at_5_diff1
      value: 52.3292
    - type: nauc_mrr_at_10_max
      value: 28.169300000000003
    - type: nauc_mrr_at_10_std
      value: -9.945500000000001
    - type: nauc_mrr_at_10_diff1
      value: 52.2672
    - type: nauc_mrr_at_20_max
      value: 28.079900000000002
    - type: nauc_mrr_at_20_std
      value: -9.9048
    - type: nauc_mrr_at_20_diff1
      value: 52.24100000000001
    - type: nauc_mrr_at_100_max
      value: 28.0893
    - type: nauc_mrr_at_100_std
      value: -9.8382
    - type: nauc_mrr_at_100_diff1
      value: 52.2779
    - type: nauc_mrr_at_1000_max
      value: 28.0878
    - type: nauc_mrr_at_1000_std
      value: -9.8445
    - type: nauc_mrr_at_1000_diff1
      value: 52.2877
    - type: main_score
      value: 52.035
    task:
      type: Retrieval
  - dataset:
      config: go
      name: MTEB CodeSearchNetCCRetrieval (go)
      revision: 6e1effa2c03723c5fde48ee912b5ee08d4f211e8
      split: test
      type: CoIR-Retrieval/CodeSearchNet-ccr
    metrics:
    - type: ndcg_at_1
      value: 27.259
    - type: ndcg_at_3
      value: 34.537
    - type: ndcg_at_5
      value: 36.658
    - type: ndcg_at_10
      value: 38.749
    - type: ndcg_at_20
      value: 40.439
    - type: ndcg_at_100
      value: 43.021
    - type: ndcg_at_1000
      value: 44.909
    - type: map_at_1
      value: 27.259
    - type: map_at_3
      value: 32.738
    - type: map_at_5
      value: 33.916000000000004
    - type: map_at_10
      value: 34.787
    - type: map_at_20
      value: 35.253
    - type: map_at_100
      value: 35.597
    - type: map_at_1000
      value: 35.66
    - type: recall_at_1
      value: 27.259
    - type: recall_at_3
      value: 39.744
    - type: recall_at_5
      value: 44.89
    - type: recall_at_10
      value: 51.317
    - type: recall_at_20
      value: 57.99100000000001
    - type: recall_at_100
      value: 72.088
    - type: recall_at_1000
      value: 87.368
    - type: precision_at_1
      value: 27.259
    - type: precision_at_3
      value: 13.248
    - type: precision_at_5
      value: 8.978
    - type: precision_at_10
      value: 5.132
    - type: precision_at_20
      value: 2.9000000000000004
    - type: precision_at_100
      value: 0.721
    - type: precision_at_1000
      value: 0.087
    - type: mrr_at_1
      value: 27.247
    - type: mrr_at_3
      value: 32.73
    - type: mrr_at_5
      value: 33.9188
    - type: mrr_at_10
      value: 34.7795
    - type: mrr_at_20
      value: 35.2462
    - type: mrr_at_100
      value: 35.5904
    - type: mrr_at_1000
      value: 35.654
    - type: nauc_ndcg_at_1_max
      value: 26.4086
    - type: nauc_ndcg_at_1_std
      value: -2.9711000000000003
    - type: nauc_ndcg_at_1_diff1
      value: 51.946099999999994
    - type: nauc_ndcg_at_3_max
      value: 25.4155
    - type: nauc_ndcg_at_3_std
      value: -2.8535999999999997
    - type: nauc_ndcg_at_3_diff1
      value: 46.7669
    - type: nauc_ndcg_at_5_max
      value: 25.0238
    - type: nauc_ndcg_at_5_std
      value: -2.5973
    - type: nauc_ndcg_at_5_diff1
      value: 46.2719
    - type: nauc_ndcg_at_10_max
      value: 24.3719
    - type: nauc_ndcg_at_10_std
      value: -2.4239
    - type: nauc_ndcg_at_10_diff1
      value: 45.5531
    - type: nauc_ndcg_at_20_max
      value: 24.2915
    - type: nauc_ndcg_at_20_std
      value: -2.0365
    - type: nauc_ndcg_at_20_diff1
      value: 45.290200000000006
    - type: nauc_ndcg_at_100_max
      value: 23.9849
    - type: nauc_ndcg_at_100_std
      value: -1.1925
    - type: nauc_ndcg_at_100_diff1
      value: 45.1382
    - type: nauc_ndcg_at_1000_max
      value: 24.3502
    - type: nauc_ndcg_at_1000_std
      value: -0.7086
    - type: nauc_ndcg_at_1000_diff1
      value: 45.550200000000004
    - type: nauc_map_at_1_max
      value: 26.4086
    - type: nauc_map_at_1_std
      value: -2.9711000000000003
    - type: nauc_map_at_1_diff1
      value: 51.946099999999994
    - type: nauc_map_at_3_max
      value: 25.6581
    - type: nauc_map_at_3_std
      value: -2.8928
    - type: nauc_map_at_3_diff1
      value: 47.9103
    - type: nauc_map_at_5_max
      value: 25.438699999999997
    - type: nauc_map_at_5_std
      value: -2.759
    - type: nauc_map_at_5_diff1
      value: 47.6395
    - type: nauc_map_at_10_max
      value: 25.167299999999997
    - type: nauc_map_at_10_std
      value: -2.6864
    - type: nauc_map_at_10_diff1
      value: 47.335100000000004
    - type: nauc_map_at_20_max
      value: 25.1492
    - type: nauc_map_at_20_std
      value: -2.5978000000000003
    - type: nauc_map_at_20_diff1
      value: 47.2833
    - type: nauc_map_at_100_max
      value: 25.094499999999996
    - type: nauc_map_at_100_std
      value: -2.5058000000000002
    - type: nauc_map_at_100_diff1
      value: 47.2631
    - type: nauc_map_at_1000_max
      value: 25.105100000000004
    - type: nauc_map_at_1000_std
      value: -2.4873
    - type: nauc_map_at_1000_diff1
      value: 47.279900000000005
    - type: nauc_recall_at_1_max
      value: 26.4086
    - type: nauc_recall_at_1_std
      value: -2.9711000000000003
    - type: nauc_recall_at_1_diff1
      value: 51.946099999999994
    - type: nauc_recall_at_3_max
      value: 24.743499999999997
    - type: nauc_recall_at_3_std
      value: -2.7411000000000003
    - type: nauc_recall_at_3_diff1
      value: 43.6461
    - type: nauc_recall_at_5_max
      value: 23.8105
    - type: nauc_recall_at_5_std
      value: -2.0951
    - type: nauc_recall_at_5_diff1
      value: 42.4182
    - type: nauc_recall_at_10_max
      value: 21.7867
    - type: nauc_recall_at_10_std
      value: -1.5507
    - type: nauc_recall_at_10_diff1
      value: 40.1507
    - type: nauc_recall_at_20_max
      value: 21.264
    - type: nauc_recall_at_20_std
      value: 0.2463
    - type: nauc_recall_at_20_diff1
      value: 38.5714
    - type: nauc_recall_at_100_max
      value: 18.4525
    - type: nauc_recall_at_100_std
      value: 7.3066
    - type: nauc_recall_at_100_diff1
      value: 35.585
    - type: nauc_recall_at_1000_max
      value: 20.769299999999998
    - type: nauc_recall_at_1000_std
      value: 24.6752
    - type: nauc_recall_at_1000_diff1
      value: 34.4382
    - type: nauc_precision_at_1_max
      value: 26.4086
    - type: nauc_precision_at_1_std
      value: -2.9711000000000003
    - type: nauc_precision_at_1_diff1
      value: 51.946099999999994
    - type: nauc_precision_at_3_max
      value: 24.743499999999997
    - type: nauc_precision_at_3_std
      value: -2.7411000000000003
    - type: nauc_precision_at_3_diff1
      value: 43.6461
    - type: nauc_precision_at_5_max
      value: 23.8105
    - type: nauc_precision_at_5_std
      value: -2.0951
    - type: nauc_precision_at_5_diff1
      value: 42.4182
    - type: nauc_precision_at_10_max
      value: 21.7867
    - type: nauc_precision_at_10_std
      value: -1.5507
    - type: nauc_precision_at_10_diff1
      value: 40.1507
    - type: nauc_precision_at_20_max
      value: 21.264
    - type: nauc_precision_at_20_std
      value: 0.2463
    - type: nauc_precision_at_20_diff1
      value: 38.5714
    - type: nauc_precision_at_100_max
      value: 18.4525
    - type: nauc_precision_at_100_std
      value: 7.3066
    - type: nauc_precision_at_100_diff1
      value: 35.585
    - type: nauc_precision_at_1000_max
      value: 20.769299999999998
    - type: nauc_precision_at_1000_std
      value: 24.6752
    - type: nauc_precision_at_1000_diff1
      value: 34.4382
    - type: nauc_mrr_at_1_max
      value: 26.4631
    - type: nauc_mrr_at_1_std
      value: -2.9343999999999997
    - type: nauc_mrr_at_1_diff1
      value: 51.9943
    - type: nauc_mrr_at_3_max
      value: 25.695
    - type: nauc_mrr_at_3_std
      value: -2.8865
    - type: nauc_mrr_at_3_diff1
      value: 47.948299999999996
    - type: nauc_mrr_at_5_max
      value: 25.461
    - type: nauc_mrr_at_5_std
      value: -2.7289999999999996
    - type: nauc_mrr_at_5_diff1
      value: 47.6623
    - type: nauc_mrr_at_10_max
      value: 25.1963
    - type: nauc_mrr_at_10_std
      value: -2.6818999999999997
    - type: nauc_mrr_at_10_diff1
      value: 47.374500000000005
    - type: nauc_mrr_at_20_max
      value: 25.178800000000003
    - type: nauc_mrr_at_20_std
      value: -2.5887000000000002
    - type: nauc_mrr_at_20_diff1
      value: 47.3199
    - type: nauc_mrr_at_100_max
      value: 25.1241
    - type: nauc_mrr_at_100_std
      value: -2.4967
    - type: nauc_mrr_at_100_diff1
      value: 47.2999
    - type: nauc_mrr_at_1000_max
      value: 25.134800000000002
    - type: nauc_mrr_at_1000_std
      value: -2.4783
    - type: nauc_mrr_at_1000_diff1
      value: 47.3167
    - type: main_score
      value: 38.749
    task:
      type: Retrieval
  - dataset:
      config: ruby
      name: MTEB CodeSearchNetCCRetrieval (ruby)
      revision: 6e1effa2c03723c5fde48ee912b5ee08d4f211e8
      split: test
      type: CoIR-Retrieval/CodeSearchNet-ccr
    metrics:
    - type: ndcg_at_1
      value: 40.92
    - type: ndcg_at_3
      value: 49.364999999999995
    - type: ndcg_at_5
      value: 51.654999999999994
    - type: ndcg_at_10
      value: 53.169999999999995
    - type: ndcg_at_20
      value: 54.64
    - type: ndcg_at_100
      value: 56.974000000000004
    - type: ndcg_at_1000
      value: 58.306999999999995
    - type: map_at_1
      value: 40.92
    - type: map_at_3
      value: 47.343
    - type: map_at_5
      value: 48.616
    - type: map_at_10
      value: 49.242000000000004
    - type: map_at_20
      value: 49.647999999999996
    - type: map_at_100
      value: 49.97
    - type: map_at_1000
      value: 50.017999999999994
    - type: recall_at_1
      value: 40.92
    - type: recall_at_3
      value: 55.193999999999996
    - type: recall_at_5
      value: 60.745000000000005
    - type: recall_at_10
      value: 65.424
    - type: recall_at_20
      value: 71.21300000000001
    - type: recall_at_100
      value: 83.822
    - type: recall_at_1000
      value: 94.44900000000001
    - type: precision_at_1
      value: 40.92
    - type: precision_at_3
      value: 18.398
    - type: precision_at_5
      value: 12.149000000000001
    - type: precision_at_10
      value: 6.542000000000001
    - type: precision_at_20
      value: 3.5610000000000004
    - type: precision_at_100
      value: 0.8380000000000001
    - type: precision_at_1000
      value: 0.094
    - type: mrr_at_1
      value: 40.9199
    - type: mrr_at_3
      value: 47.3434
    - type: mrr_at_5
      value: 48.6162
    - type: mrr_at_10
      value: 49.2421
    - type: mrr_at_20
      value: 49.6524
    - type: mrr_at_100
      value: 49.9694
    - type: mrr_at_1000
      value: 50.017999999999994
    - type: nauc_ndcg_at_1_max
      value: 28.5367
    - type: nauc_ndcg_at_1_std
      value: -8.2024
    - type: nauc_ndcg_at_1_diff1
      value: 59.920399999999994
    - type: nauc_ndcg_at_3_max
      value: 29.583399999999997
    - type: nauc_ndcg_at_3_std
      value: -10.276499999999999
    - type: nauc_ndcg_at_3_diff1
      value: 53.3108
    - type: nauc_ndcg_at_5_max
      value: 29.124299999999998
    - type: nauc_ndcg_at_5_std
      value: -9.9282
    - type: nauc_ndcg_at_5_diff1
      value: 53.1591
    - type: nauc_ndcg_at_10_max
      value: 28.778599999999997
    - type: nauc_ndcg_at_10_std
      value: -10.319799999999999
    - type: nauc_ndcg_at_10_diff1
      value: 53.244499999999995
    - type: nauc_ndcg_at_20_max
      value: 28.8719
    - type: nauc_ndcg_at_20_std
      value: -9.7272
    - type: nauc_ndcg_at_20_diff1
      value: 53.3575
    - type: nauc_ndcg_at_100_max
      value: 28.8624
    - type: nauc_ndcg_at_100_std
      value: -9.3621
    - type: nauc_ndcg_at_100_diff1
      value: 53.322599999999994
    - type: nauc_ndcg_at_1000_max
      value: 28.876400000000004
    - type: nauc_ndcg_at_1000_std
      value: -9.3757
    - type: nauc_ndcg_at_1000_diff1
      value: 53.5029
    - type: nauc_map_at_1_max
      value: 28.5367
    - type: nauc_map_at_1_std
      value: -8.2024
    - type: nauc_map_at_1_diff1
      value: 59.920399999999994
    - type: nauc_map_at_3_max
      value: 29.373500000000003
    - type: nauc_map_at_3_std
      value: -9.7647
    - type: nauc_map_at_3_diff1
      value: 54.8768
    - type: nauc_map_at_5_max
      value: 29.1429
    - type: nauc_map_at_5_std
      value: -9.5913
    - type: nauc_map_at_5_diff1
      value: 54.8183
    - type: nauc_map_at_10_max
      value: 29.0079
    - type: nauc_map_at_10_std
      value: -9.7633
    - type: nauc_map_at_10_diff1
      value: 54.87180000000001
    - type: nauc_map_at_20_max
      value: 29.004
    - type: nauc_map_at_20_std
      value: -9.609399999999999
    - type: nauc_map_at_20_diff1
      value: 54.8733
    - type: nauc_map_at_100_max
      value: 28.961100000000002
    - type: nauc_map_at_100_std
      value: -9.586500000000001
    - type: nauc_map_at_100_diff1
      value: 54.85719999999999
    - type: nauc_map_at_1000_max
      value: 28.957
    - type: nauc_map_at_1000_std
      value: -9.5861
    - type: nauc_map_at_1000_diff1
      value: 54.8685
    - type: nauc_recall_at_1_max
      value: 28.5367
    - type: nauc_recall_at_1_std
      value: -8.2024
    - type: nauc_recall_at_1_diff1
      value: 59.920399999999994
    - type: nauc_recall_at_3_max
      value: 30.198900000000002
    - type: nauc_recall_at_3_std
      value: -11.8281
    - type: nauc_recall_at_3_diff1
      value: 48.5911
    - type: nauc_recall_at_5_max
      value: 28.938000000000002
    - type: nauc_recall_at_5_std
      value: -10.9165
    - type: nauc_recall_at_5_diff1
      value: 47.8612
    - type: nauc_recall_at_10_max
      value: 27.6793
    - type: nauc_recall_at_10_std
      value: -12.281400000000001
    - type: nauc_recall_at_10_diff1
      value: 47.665400000000005
    - type: nauc_recall_at_20_max
      value: 28.2941
    - type: nauc_recall_at_20_std
      value: -9.5387
    - type: nauc_recall_at_20_diff1
      value: 47.875
    - type: nauc_recall_at_100_max
      value: 29.1692
    - type: nauc_recall_at_100_std
      value: -4.8877999999999995
    - type: nauc_recall_at_100_diff1
      value: 44.8146
    - type: nauc_recall_at_1000_max
      value: 32.1351
    - type: nauc_recall_at_1000_std
      value: 2.178
    - type: nauc_recall_at_1000_diff1
      value: 35.842600000000004
    - type: nauc_precision_at_1_max
      value: 28.5367
    - type: nauc_precision_at_1_std
      value: -8.2024
    - type: nauc_precision_at_1_diff1
      value: 59.920399999999994
    - type: nauc_precision_at_3_max
      value: 30.198900000000002
    - type: nauc_precision_at_3_std
      value: -11.8281
    - type: nauc_precision_at_3_diff1
      value: 48.5911
    - type: nauc_precision_at_5_max
      value: 28.938000000000002
    - type: nauc_precision_at_5_std
      value: -10.9165
    - type: nauc_precision_at_5_diff1
      value: 47.8612
    - type: nauc_precision_at_10_max
      value: 27.6793
    - type: nauc_precision_at_10_std
      value: -12.281400000000001
    - type: nauc_precision_at_10_diff1
      value: 47.665400000000005
    - type: nauc_precision_at_20_max
      value: 28.2941
    - type: nauc_precision_at_20_std
      value: -9.5387
    - type: nauc_precision_at_20_diff1
      value: 47.875
    - type: nauc_precision_at_100_max
      value: 29.1692
    - type: nauc_precision_at_100_std
      value: -4.8877999999999995
    - type: nauc_precision_at_100_diff1
      value: 44.8146
    - type: nauc_precision_at_1000_max
      value: 32.1351
    - type: nauc_precision_at_1000_std
      value: 2.178
    - type: nauc_precision_at_1000_diff1
      value: 35.842600000000004
    - type: nauc_mrr_at_1_max
      value: 28.6205
    - type: nauc_mrr_at_1_std
      value: -8.180900000000001
    - type: nauc_mrr_at_1_diff1
      value: 59.920399999999994
    - type: nauc_mrr_at_3_max
      value: 29.416900000000002
    - type: nauc_mrr_at_3_std
      value: -9.7536
    - type: nauc_mrr_at_3_diff1
      value: 54.8768
    - type: nauc_mrr_at_5_max
      value: 29.187
    - type: nauc_mrr_at_5_std
      value: -9.58
    - type: nauc_mrr_at_5_diff1
      value: 54.8183
    - type: nauc_mrr_at_10_max
      value: 29.0523
    - type: nauc_mrr_at_10_std
      value: -9.7519
    - type: nauc_mrr_at_10_diff1
      value: 54.87180000000001
    - type: nauc_mrr_at_20_max
      value: 29.0395
    - type: nauc_mrr_at_20_std
      value: -9.5921
    - type: nauc_mrr_at_20_diff1
      value: 54.8737
    - type: nauc_mrr_at_100_max
      value: 29.0069
    - type: nauc_mrr_at_100_std
      value: -9.5772
    - type: nauc_mrr_at_100_diff1
      value: 54.8585
    - type: nauc_mrr_at_1000_max
      value: 29.0016
    - type: nauc_mrr_at_1000_std
      value: -9.574399999999999
    - type: nauc_mrr_at_1000_diff1
      value: 54.8686
    - type: main_score
      value: 53.169999999999995
    task:
      type: Retrieval
  - dataset:
      config: java
      name: MTEB CodeSearchNetCCRetrieval (java)
      revision: 6e1effa2c03723c5fde48ee912b5ee08d4f211e8
      split: test
      type: CoIR-Retrieval/CodeSearchNet-ccr
    metrics:
    - type: ndcg_at_1
      value: 38.01
    - type: ndcg_at_3
      value: 46.611999999999995
    - type: ndcg_at_5
      value: 48.644999999999996
    - type: ndcg_at_10
      value: 50.722
    - type: ndcg_at_20
      value: 52.168000000000006
    - type: ndcg_at_100
      value: 54.284
    - type: ndcg_at_1000
      value: 55.64
    - type: map_at_1
      value: 38.01
    - type: map_at_3
      value: 44.529
    - type: map_at_5
      value: 45.657
    - type: map_at_10
      value: 46.522999999999996
    - type: map_at_20
      value: 46.921
    - type: map_at_100
      value: 47.21
    - type: map_at_1000
      value: 47.257
    - type: recall_at_1
      value: 38.01
    - type: recall_at_3
      value: 52.624
    - type: recall_at_5
      value: 57.562999999999995
    - type: recall_at_10
      value: 63.943000000000005
    - type: recall_at_20
      value: 69.649
    - type: recall_at_100
      value: 81.114
    - type: recall_at_1000
      value: 92.03099999999999
    - type: precision_at_1
      value: 38.01
    - type: precision_at_3
      value: 17.541
    - type: precision_at_5
      value: 11.513
    - type: precision_at_10
      value: 6.394
    - type: precision_at_20
      value: 3.4819999999999998
    - type: precision_at_100
      value: 0.8109999999999999
    - type: precision_at_1000
      value: 0.092
    - type: mrr_at_1
      value: 38.0739
    - type: mrr_at_3
      value: 44.5626
    - type: mrr_at_5
      value: 45.6863
    - type: mrr_at_10
      value: 46.5541
    - type: mrr_at_20
      value: 46.9528
    - type: mrr_at_100
      value: 47.2419
    - type: mrr_at_1000
      value: 47.2883
    - type: nauc_ndcg_at_1_max
      value: 29.1715
    - type: nauc_ndcg_at_1_std
      value: -8.383799999999999
    - type: nauc_ndcg_at_1_diff1
      value: 56.6392
    - type: nauc_ndcg_at_3_max
      value: 31.600499999999997
    - type: nauc_ndcg_at_3_std
      value: -6.8286
    - type: nauc_ndcg_at_3_diff1
      value: 51.9436
    - type: nauc_ndcg_at_5_max
      value: 31.446099999999998
    - type: nauc_ndcg_at_5_std
      value: -6.3155
    - type: nauc_ndcg_at_5_diff1
      value: 51.4265
    - type: nauc_ndcg_at_10_max
      value: 31.484
    - type: nauc_ndcg_at_10_std
      value: -5.7347
    - type: nauc_ndcg_at_10_diff1
      value: 51.254
    - type: nauc_ndcg_at_20_max
      value: 31.5004
    - type: nauc_ndcg_at_20_std
      value: -5.141
    - type: nauc_ndcg_at_20_diff1
      value: 50.8621
    - type: nauc_ndcg_at_100_max
      value: 31.4661
    - type: nauc_ndcg_at_100_std
      value: -4.9658
    - type: nauc_ndcg_at_100_diff1
      value: 50.9602
    - type: nauc_ndcg_at_1000_max
      value: 31.544299999999996
    - type: nauc_ndcg_at_1000_std
      value: -5.0944
    - type: nauc_ndcg_at_1000_diff1
      value: 51.29559999999999
    - type: nauc_map_at_1_max
      value: 29.1715
    - type: nauc_map_at_1_std
      value: -8.383799999999999
    - type: nauc_map_at_1_diff1
      value: 56.6392
    - type: nauc_map_at_3_max
      value: 31.0216
    - type: nauc_map_at_3_std
      value: -7.2461
    - type: nauc_map_at_3_diff1
      value: 53.0413
    - type: nauc_map_at_5_max
      value: 30.944300000000002
    - type: nauc_map_at_5_std
      value: -6.9658999999999995
    - type: nauc_map_at_5_diff1
      value: 52.7782
    - type: nauc_map_at_10_max
      value: 30.9525
    - type: nauc_map_at_10_std
      value: -6.7453
    - type: nauc_map_at_10_diff1
      value: 52.7226
    - type: nauc_map_at_20_max
      value: 30.9542
    - type: nauc_map_at_20_std
      value: -6.5941
    - type: nauc_map_at_20_diff1
      value: 52.6293
    - type: nauc_map_at_100_max
      value: 30.9493
    - type: nauc_map_at_100_std
      value: -6.5776
    - type: nauc_map_at_100_diff1
      value: 52.65069999999999
    - type: nauc_map_at_1000_max
      value: 30.9515
    - type: nauc_map_at_1000_std
      value: -6.5804
    - type: nauc_map_at_1000_diff1
      value: 52.662299999999995
    - type: nauc_recall_at_1_max
      value: 29.1715
    - type: nauc_recall_at_1_std
      value: -8.383799999999999
    - type: nauc_recall_at_1_diff1
      value: 56.6392
    - type: nauc_recall_at_3_max
      value: 33.317600000000006
    - type: nauc_recall_at_3_std
      value: -5.569500000000001
    - type: nauc_recall_at_3_diff1
      value: 48.6968
    - type: nauc_recall_at_5_max
      value: 32.9542
    - type: nauc_recall_at_5_std
      value: -4.2065
    - type: nauc_recall_at_5_diff1
      value: 47.1643
    - type: nauc_recall_at_10_max
      value: 33.253
    - type: nauc_recall_at_10_std
      value: -1.9276000000000002
    - type: nauc_recall_at_10_diff1
      value: 46.1287
    - type: nauc_recall_at_20_max
      value: 33.5398
    - type: nauc_recall_at_20_std
      value: 1.4168
    - type: nauc_recall_at_20_diff1
      value: 43.5924
    - type: nauc_recall_at_100_max
      value: 34.0873
    - type: nauc_recall_at_100_std
      value: 6.0484
    - type: nauc_recall_at_100_diff1
      value: 41.1325
    - type: nauc_recall_at_1000_max
      value: 39.7041
    - type: nauc_recall_at_1000_std
      value: 15.0263
    - type: nauc_recall_at_1000_diff1
      value: 39.2976
    - type: nauc_precision_at_1_max
      value: 29.1715
    - type: nauc_precision_at_1_std
      value: -8.383799999999999
    - type: nauc_precision_at_1_diff1
      value: 56.6392
    - type: nauc_precision_at_3_max
      value: 33.317600000000006
    - type: nauc_precision_at_3_std
      value: -5.569500000000001
    - type: nauc_precision_at_3_diff1
      value: 48.6968
    - type: nauc_precision_at_5_max
      value: 32.9542
    - type: nauc_precision_at_5_std
      value: -4.2065
    - type: nauc_precision_at_5_diff1
      value: 47.1643
    - type: nauc_precision_at_10_max
      value: 33.253
    - type: nauc_precision_at_10_std
      value: -1.9276000000000002
    - type: nauc_precision_at_10_diff1
      value: 46.1287
    - type: nauc_precision_at_20_max
      value: 33.5398
    - type: nauc_precision_at_20_std
      value: 1.4168
    - type: nauc_precision_at_20_diff1
      value: 43.5924
    - type: nauc_precision_at_100_max
      value: 34.0873
    - type: nauc_precision_at_100_std
      value: 6.0484
    - type: nauc_precision_at_100_diff1
      value: 41.1325
    - type: nauc_precision_at_1000_max
      value: 39.7041
    - type: nauc_precision_at_1000_std
      value: 15.0263
    - type: nauc_precision_at_1000_diff1
      value: 39.2976
    - type: nauc_mrr_at_1_max
      value: 29.1889
    - type: nauc_mrr_at_1_std
      value: -8.3731
    - type: nauc_mrr_at_1_diff1
      value: 56.4441
    - type: nauc_mrr_at_3_max
      value: 31.034
    - type: nauc_mrr_at_3_std
      value: -7.2402
    - type: nauc_mrr_at_3_diff1
      value: 52.9257
    - type: nauc_mrr_at_5_max
      value: 30.9601
    - type: nauc_mrr_at_5_std
      value: -6.969799999999999
    - type: nauc_mrr_at_5_diff1
      value: 52.6602
    - type: nauc_mrr_at_10_max
      value: 30.965300000000003
    - type: nauc_mrr_at_10_std
      value: -6.741700000000001
    - type: nauc_mrr_at_10_diff1
      value: 52.6096
    - type: nauc_mrr_at_20_max
      value: 30.9681
    - type: nauc_mrr_at_20_std
      value: -6.5917
    - type: nauc_mrr_at_20_diff1
      value: 52.518299999999996
    - type: nauc_mrr_at_100_max
      value: 30.9633
    - type: nauc_mrr_at_100_std
      value: -6.575200000000001
    - type: nauc_mrr_at_100_diff1
      value: 52.539
    - type: nauc_mrr_at_1000_max
      value: 30.965500000000002
    - type: nauc_mrr_at_1000_std
      value: -6.578
    - type: nauc_mrr_at_1000_diff1
      value: 52.550399999999996
    - type: main_score
      value: 50.722
    task:
      type: Retrieval
  - dataset:
      config: php
      name: MTEB CodeSearchNetCCRetrieval (php)
      revision: 6e1effa2c03723c5fde48ee912b5ee08d4f211e8
      split: test
      type: CoIR-Retrieval/CodeSearchNet-ccr
    metrics:
    - type: ndcg_at_1
      value: 27.915
    - type: ndcg_at_3
      value: 35.388
    - type: ndcg_at_5
      value: 37.406
    - type: ndcg_at_10
      value: 39.660000000000004
    - type: ndcg_at_20
      value: 41.202
    - type: ndcg_at_100
      value: 43.916
    - type: ndcg_at_1000
      value: 45.867000000000004
    - type: map_at_1
      value: 27.915
    - type: map_at_3
      value: 33.545
    - type: map_at_5
      value: 34.666999999999994
    - type: map_at_10
      value: 35.606
    - type: map_at_20
      value: 36.032
    - type: map_at_100
      value: 36.399
    - type: map_at_1000
      value: 36.464999999999996
    - type: recall_at_1
      value: 27.915
    - type: recall_at_3
      value: 40.724
    - type: recall_at_5
      value: 45.612
    - type: recall_at_10
      value: 52.54
    - type: recall_at_20
      value: 58.61300000000001
    - type: recall_at_100
      value: 73.369
    - type: recall_at_1000
      value: 89.14699999999999
    - type: precision_at_1
      value: 27.915
    - type: precision_at_3
      value: 13.575000000000001
    - type: precision_at_5
      value: 9.122
    - type: precision_at_10
      value: 5.2540000000000004
    - type: precision_at_20
      value: 2.931
    - type: precision_at_100
      value: 0.734
    - type: precision_at_1000
      value: 0.089
    - type: mrr_at_1
      value: 27.8935
    - type: mrr_at_3
      value: 33.529599999999995
    - type: mrr_at_5
      value: 34.6563
    - type: mrr_at_10
      value: 35.596
    - type: mrr_at_20
      value: 36.0216
    - type: mrr_at_100
      value: 36.3884
    - type: mrr_at_1000
      value: 36.4547
    - type: nauc_ndcg_at_1_max
      value: 23.1709
    - type: nauc_ndcg_at_1_std
      value: -5.9072
    - type: nauc_ndcg_at_1_diff1
      value: 49.3299
    - type: nauc_ndcg_at_3_max
      value: 22.8661
    - type: nauc_ndcg_at_3_std
      value: -5.095899999999999
    - type: nauc_ndcg_at_3_diff1
      value: 43.9897
    - type: nauc_ndcg_at_5_max
      value: 22.5328
    - type: nauc_ndcg_at_5_std
      value: -4.7091
    - type: nauc_ndcg_at_5_diff1
      value: 43.3944
    - type: nauc_ndcg_at_10_max
      value: 21.9501
    - type: nauc_ndcg_at_10_std
      value: -4.162
    - type: nauc_ndcg_at_10_diff1
      value: 42.3066
    - type: nauc_ndcg_at_20_max
      value: 21.9053
    - type: nauc_ndcg_at_20_std
      value: -3.5355999999999996
    - type: nauc_ndcg_at_20_diff1
      value: 42.1593
    - type: nauc_ndcg_at_100_max
      value: 21.7083
    - type: nauc_ndcg_at_100_std
      value: -2.9722999999999997
    - type: nauc_ndcg_at_100_diff1
      value: 41.9229
    - type: nauc_ndcg_at_1000_max
      value: 21.9067
    - type: nauc_ndcg_at_1000_std
      value: -2.984
    - type: nauc_ndcg_at_1000_diff1
      value: 42.4281
    - type: nauc_map_at_1_max
      value: 23.1709
    - type: nauc_map_at_1_std
      value: -5.9072
    - type: nauc_map_at_1_diff1
      value: 49.3299
    - type: nauc_map_at_3_max
      value: 22.9725
    - type: nauc_map_at_3_std
      value: -5.292199999999999
    - type: nauc_map_at_3_diff1
      value: 45.2572
    - type: nauc_map_at_5_max
      value: 22.7878
    - type: nauc_map_at_5_std
      value: -5.0855999999999995
    - type: nauc_map_at_5_diff1
      value: 44.9362
    - type: nauc_map_at_10_max
      value: 22.554299999999998
    - type: nauc_map_at_10_std
      value: -4.855700000000001
    - type: nauc_map_at_10_diff1
      value: 44.472899999999996
    - type: nauc_map_at_20_max
      value: 22.5365
    - type: nauc_map_at_20_std
      value: -4.7015
    - type: nauc_map_at_20_diff1
      value: 44.441900000000004
    - type: nauc_map_at_100_max
      value: 22.5246
    - type: nauc_map_at_100_std
      value: -4.6318
    - type: nauc_map_at_100_diff1
      value: 44.4182
    - type: nauc_map_at_1000_max
      value: 22.531200000000002
    - type: nauc_map_at_1000_std
      value: -4.6294
    - type: nauc_map_at_1000_diff1
      value: 44.4336
    - type: nauc_recall_at_1_max
      value: 23.1709
    - type: nauc_recall_at_1_std
      value: -5.9072
    - type: nauc_recall_at_1_diff1
      value: 49.3299
    - type: nauc_recall_at_3_max
      value: 22.5576
    - type: nauc_recall_at_3_std
      value: -4.5496
    - type: nauc_recall_at_3_diff1
      value: 40.4722
    - type: nauc_recall_at_5_max
      value: 21.755
    - type: nauc_recall_at_5_std
      value: -3.5854
    - type: nauc_recall_at_5_diff1
      value: 38.9703
    - type: nauc_recall_at_10_max
      value: 19.8814
    - type: nauc_recall_at_10_std
      value: -1.8668
    - type: nauc_recall_at_10_diff1
      value: 35.5164
    - type: nauc_recall_at_20_max
      value: 19.6191
    - type: nauc_recall_at_20_std
      value: 1.0138
    - type: nauc_recall_at_20_diff1
      value: 34.443
    - type: nauc_recall_at_100_max
      value: 17.1186
    - type: nauc_recall_at_100_std
      value: 6.7912
    - type: nauc_recall_at_100_diff1
      value: 30.006100000000004
    - type: nauc_recall_at_1000_max
      value: 16.4494
    - type: nauc_recall_at_1000_std
      value: 17.0286
    - type: nauc_recall_at_1000_diff1
      value: 28.3205
    - type: nauc_precision_at_1_max
      value: 23.1709
    - type: nauc_precision_at_1_std
      value: -5.9072
    - type: nauc_precision_at_1_diff1
      value: 49.3299
    - type: nauc_precision_at_3_max
      value: 22.5576
    - type: nauc_precision_at_3_std
      value: -4.5496
    - type: nauc_precision_at_3_diff1
      value: 40.4722
    - type: nauc_precision_at_5_max
      value: 21.755
    - type: nauc_precision_at_5_std
      value: -3.5854
    - type: nauc_precision_at_5_diff1
      value: 38.9703
    - type: nauc_precision_at_10_max
      value: 19.8814
    - type: nauc_precision_at_10_std
      value: -1.8668
    - type: nauc_precision_at_10_diff1
      value: 35.5164
    - type: nauc_precision_at_20_max
      value: 19.6191
    - type: nauc_precision_at_20_std
      value: 1.0138
    - type: nauc_precision_at_20_diff1
      value: 34.443
    - type: nauc_precision_at_100_max
      value: 17.1186
    - type: nauc_precision_at_100_std
      value: 6.7912
    - type: nauc_precision_at_100_diff1
      value: 30.006100000000004
    - type: nauc_precision_at_1000_max
      value: 16.4494
    - type: nauc_precision_at_1000_std
      value: 17.0286
    - type: nauc_precision_at_1000_diff1
      value: 28.3205
    - type: nauc_mrr_at_1_max
      value: 23.1792
    - type: nauc_mrr_at_1_std
      value: -5.8884
    - type: nauc_mrr_at_1_diff1
      value: 49.411899999999996
    - type: nauc_mrr_at_3_max
      value: 22.9617
    - type: nauc_mrr_at_3_std
      value: -5.2925
    - type: nauc_mrr_at_3_diff1
      value: 45.2913
    - type: nauc_mrr_at_5_max
      value: 22.7693
    - type: nauc_mrr_at_5_std
      value: -5.0912
    - type: nauc_mrr_at_5_diff1
      value: 44.966699999999996
    - type: nauc_mrr_at_10_max
      value: 22.5429
    - type: nauc_mrr_at_10_std
      value: -4.8534
    - type: nauc_mrr_at_10_diff1
      value: 44.5081
    - type: nauc_mrr_at_20_max
      value: 22.5247
    - type: nauc_mrr_at_20_std
      value: -4.7001
    - type: nauc_mrr_at_20_diff1
      value: 44.4776
    - type: nauc_mrr_at_100_max
      value: 22.5126
    - type: nauc_mrr_at_100_std
      value: -4.6305
    - type: nauc_mrr_at_100_diff1
      value: 44.453900000000004
    - type: nauc_mrr_at_1000_max
      value: 22.5191
    - type: nauc_mrr_at_1000_std
      value: -4.6281
    - type: nauc_mrr_at_1000_diff1
      value: 44.469300000000004
    - type: main_score
      value: 39.660000000000004
    task:
      type: Retrieval
  - dataset:
      config: python
      name: MTEB CodeSearchNetRetrieval (python)
      revision: fdc6a9e39575768c27eb8a2a5f702bf846eb4759
      split: test
      type: code-search-net/code_search_net
    metrics:
    - type: ndcg_at_1
      value: 71.3
    - type: ndcg_at_3
      value: 80.46600000000001
    - type: ndcg_at_5
      value: 82.657
    - type: ndcg_at_10
      value: 83.633
    - type: ndcg_at_20
      value: 84.108
    - type: ndcg_at_100
      value: 84.532
    - type: ndcg_at_1000
      value: 84.651
    - type: map_at_1
      value: 71.3
    - type: map_at_3
      value: 78.3
    - type: map_at_5
      value: 79.52
    - type: map_at_10
      value: 79.926
    - type: map_at_20
      value: 80.054
    - type: map_at_100
      value: 80.119
    - type: map_at_1000
      value: 80.124
    - type: recall_at_1
      value: 71.3
    - type: recall_at_3
      value: 86.7
    - type: recall_at_5
      value: 92.0
    - type: recall_at_10
      value: 95.0
    - type: recall_at_20
      value: 96.89999999999999
    - type: recall_at_100
      value: 99.1
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 71.3
    - type: precision_at_3
      value: 28.9
    - type: precision_at_5
      value: 18.4
    - type: precision_at_10
      value: 9.5
    - type: precision_at_20
      value: 4.845
    - type: precision_at_100
      value: 0.991
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 71.3
    - type: mrr_at_3
      value: 78.3
    - type: mrr_at_5
      value: 79.52
    - type: mrr_at_10
      value: 79.9264
    - type: mrr_at_20
      value: 80.0537
    - type: mrr_at_100
      value: 80.119
    - type: mrr_at_1000
      value: 80.1241
    - type: nauc_ndcg_at_1_max
      value: 42.5887
    - type: nauc_ndcg_at_1_std
      value: -4.7713
    - type: nauc_ndcg_at_1_diff1
      value: 71.5211
    - type: nauc_ndcg_at_3_max
      value: 42.682500000000005
    - type: nauc_ndcg_at_3_std
      value: -9.7713
    - type: nauc_ndcg_at_3_diff1
      value: 70.09450000000001
    - type: nauc_ndcg_at_5_max
      value: 42.8369
    - type: nauc_ndcg_at_5_std
      value: -8.636000000000001
    - type: nauc_ndcg_at_5_diff1
      value: 70.06569999999999
    - type: nauc_ndcg_at_10_max
      value: 42.0272
    - type: nauc_ndcg_at_10_std
      value: -7.7864
    - type: nauc_ndcg_at_10_diff1
      value: 69.647
    - type: nauc_ndcg_at_20_max
      value: 42.7338
    - type: nauc_ndcg_at_20_std
      value: -7.842300000000001
    - type: nauc_ndcg_at_20_diff1
      value: 69.8122
    - type: nauc_ndcg_at_100_max
      value: 42.7575
    - type: nauc_ndcg_at_100_std
      value: -7.330299999999999
    - type: nauc_ndcg_at_100_diff1
      value: 69.9872
    - type: nauc_ndcg_at_1000_max
      value: 42.6322
    - type: nauc_ndcg_at_1000_std
      value: -7.4643
    - type: nauc_ndcg_at_1000_diff1
      value: 70.0635
    - type: nauc_map_at_1_max
      value: 42.5887
    - type: nauc_map_at_1_std
      value: -4.7713
    - type: nauc_map_at_1_diff1
      value: 71.5211
    - type: nauc_map_at_3_max
      value: 42.5893
    - type: nauc_map_at_3_std
      value: -8.2772
    - type: nauc_map_at_3_diff1
      value: 70.3236
    - type: nauc_map_at_5_max
      value: 42.686099999999996
    - type: nauc_map_at_5_std
      value: -7.6014
    - type: nauc_map_at_5_diff1
      value: 70.284
    - type: nauc_map_at_10_max
      value: 42.4008
    - type: nauc_map_at_10_std
      value: -7.2528
    - type: nauc_map_at_10_diff1
      value: 70.1571
    - type: nauc_map_at_20_max
      value: 42.5568
    - type: nauc_map_at_20_std
      value: -7.264900000000001
    - type: nauc_map_at_20_diff1
      value: 70.2095
    - type: nauc_map_at_100_max
      value: 42.5674
    - type: nauc_map_at_100_std
      value: -7.2189000000000005
    - type: nauc_map_at_100_diff1
      value: 70.238
    - type: nauc_map_at_1000_max
      value: 42.564600000000006
    - type: nauc_map_at_1000_std
      value: -7.217899999999999
    - type: nauc_map_at_1000_diff1
      value: 70.2391
    - type: nauc_recall_at_1_max
      value: 42.5887
    - type: nauc_recall_at_1_std
      value: -4.7713
    - type: nauc_recall_at_1_diff1
      value: 71.5211
    - type: nauc_recall_at_3_max
      value: 43.1314
    - type: nauc_recall_at_3_std
      value: -16.2854
    - type: nauc_recall_at_3_diff1
      value: 69.22319999999999
    - type: nauc_recall_at_5_max
      value: 43.869
    - type: nauc_recall_at_5_std
      value: -15.228800000000001
    - type: nauc_recall_at_5_diff1
      value: 68.9332
    - type: nauc_recall_at_10_max
      value: 37.211
    - type: nauc_recall_at_10_std
      value: -12.085899999999999
    - type: nauc_recall_at_10_diff1
      value: 64.212
    - type: nauc_recall_at_20_max
      value: 47.346500000000006
    - type: nauc_recall_at_20_std
      value: -15.5748
    - type: nauc_recall_at_20_diff1
      value: 63.3866
    - type: nauc_recall_at_100_max
      value: 58.667899999999996
    - type: nauc_recall_at_100_std
      value: 12.8333
    - type: nauc_recall_at_100_diff1
      value: 60.0633
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 42.5887
    - type: nauc_precision_at_1_std
      value: -4.7713
    - type: nauc_precision_at_1_diff1
      value: 71.5211
    - type: nauc_precision_at_3_max
      value: 43.1314
    - type: nauc_precision_at_3_std
      value: -16.2854
    - type: nauc_precision_at_3_diff1
      value: 69.22319999999999
    - type: nauc_precision_at_5_max
      value: 43.869
    - type: nauc_precision_at_5_std
      value: -15.228800000000001
    - type: nauc_precision_at_5_diff1
      value: 68.9332
    - type: nauc_precision_at_10_max
      value: 37.211
    - type: nauc_precision_at_10_std
      value: -12.085899999999999
    - type: nauc_precision_at_10_diff1
      value: 64.212
    - type: nauc_precision_at_20_max
      value: 47.346500000000006
    - type: nauc_precision_at_20_std
      value: -15.5748
    - type: nauc_precision_at_20_diff1
      value: 63.3866
    - type: nauc_precision_at_100_max
      value: 58.667899999999996
    - type: nauc_precision_at_100_std
      value: 12.8333
    - type: nauc_precision_at_100_diff1
      value: 60.0633
    - type: nauc_precision_at_1000_max
      value: .nan
    - type: nauc_precision_at_1000_std
      value: .nan
    - type: nauc_precision_at_1000_diff1
      value: .nan
    - type: nauc_mrr_at_1_max
      value: 42.5887
    - type: nauc_mrr_at_1_std
      value: -4.7713
    - type: nauc_mrr_at_1_diff1
      value: 71.5211
    - type: nauc_mrr_at_3_max
      value: 42.5893
    - type: nauc_mrr_at_3_std
      value: -8.2772
    - type: nauc_mrr_at_3_diff1
      value: 70.3236
    - type: nauc_mrr_at_5_max
      value: 42.686099999999996
    - type: nauc_mrr_at_5_std
      value: -7.6014
    - type: nauc_mrr_at_5_diff1
      value: 70.284
    - type: nauc_mrr_at_10_max
      value: 42.4008
    - type: nauc_mrr_at_10_std
      value: -7.2528
    - type: nauc_mrr_at_10_diff1
      value: 70.1571
    - type: nauc_mrr_at_20_max
      value: 42.5568
    - type: nauc_mrr_at_20_std
      value: -7.264900000000001
    - type: nauc_mrr_at_20_diff1
      value: 70.2095
    - type: nauc_mrr_at_100_max
      value: 42.5674
    - type: nauc_mrr_at_100_std
      value: -7.2189000000000005
    - type: nauc_mrr_at_100_diff1
      value: 70.238
    - type: nauc_mrr_at_1000_max
      value: 42.564600000000006
    - type: nauc_mrr_at_1000_std
      value: -7.217899999999999
    - type: nauc_mrr_at_1000_diff1
      value: 70.2391
    - type: main_score
      value: 83.633
    task:
      type: Retrieval
  - dataset:
      config: javascript
      name: MTEB CodeSearchNetRetrieval (javascript)
      revision: fdc6a9e39575768c27eb8a2a5f702bf846eb4759
      split: test
      type: code-search-net/code_search_net
    metrics:
    - type: ndcg_at_1
      value: 61.4
    - type: ndcg_at_3
      value: 69.833
    - type: ndcg_at_5
      value: 71.675
    - type: ndcg_at_10
      value: 72.83699999999999
    - type: ndcg_at_20
      value: 73.56899999999999
    - type: ndcg_at_100
      value: 74.50099999999999
    - type: ndcg_at_1000
      value: 75.473
    - type: map_at_1
      value: 61.4
    - type: map_at_3
      value: 67.80000000000001
    - type: map_at_5
      value: 68.815
    - type: map_at_10
      value: 69.294
    - type: map_at_20
      value: 69.49499999999999
    - type: map_at_100
      value: 69.618
    - type: map_at_1000
      value: 69.645
    - type: recall_at_1
      value: 61.4
    - type: recall_at_3
      value: 75.7
    - type: recall_at_5
      value: 80.2
    - type: recall_at_10
      value: 83.8
    - type: recall_at_20
      value: 86.7
    - type: recall_at_100
      value: 91.8
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 61.4
    - type: precision_at_3
      value: 25.233
    - type: precision_at_5
      value: 16.04
    - type: precision_at_10
      value: 8.38
    - type: precision_at_20
      value: 4.335
    - type: precision_at_100
      value: 0.918
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 61.4
    - type: mrr_at_3
      value: 67.80000000000001
    - type: mrr_at_5
      value: 68.815
    - type: mrr_at_10
      value: 69.294
    - type: mrr_at_20
      value: 69.4947
    - type: mrr_at_100
      value: 69.6181
    - type: mrr_at_1000
      value: 69.645
    - type: nauc_ndcg_at_1_max
      value: 56.7217
    - type: nauc_ndcg_at_1_std
      value: 24.8593
    - type: nauc_ndcg_at_1_diff1
      value: 71.9101
    - type: nauc_ndcg_at_3_max
      value: 65.2032
    - type: nauc_ndcg_at_3_std
      value: 32.0444
    - type: nauc_ndcg_at_3_diff1
      value: 70.0416
    - type: nauc_ndcg_at_5_max
      value: 66.5758
    - type: nauc_ndcg_at_5_std
      value: 36.1929
    - type: nauc_ndcg_at_5_diff1
      value: 70.3931
    - type: nauc_ndcg_at_10_max
      value: 66.5108
    - type: nauc_ndcg_at_10_std
      value: 36.121199999999995
    - type: nauc_ndcg_at_10_diff1
      value: 70.6475
    - type: nauc_ndcg_at_20_max
      value: 66.7371
    - type: nauc_ndcg_at_20_std
      value: 36.5925
    - type: nauc_ndcg_at_20_diff1
      value: 70.8488
    - type: nauc_ndcg_at_100_max
      value: 66.2407
    - type: nauc_ndcg_at_100_std
      value: 37.0769
    - type: nauc_ndcg_at_100_diff1
      value: 70.5349
    - type: nauc_ndcg_at_1000_max
      value: 65.2728
    - type: nauc_ndcg_at_1000_std
      value: 34.956199999999995
    - type: nauc_ndcg_at_1000_diff1
      value: 70.6395
    - type: nauc_map_at_1_max
      value: 56.7217
    - type: nauc_map_at_1_std
      value: 24.8593
    - type: nauc_map_at_1_diff1
      value: 71.9101
    - type: nauc_map_at_3_max
      value: 63.0821
    - type: nauc_map_at_3_std
      value: 30.2166
    - type: nauc_map_at_3_diff1
      value: 70.4667
    - type: nauc_map_at_5_max
      value: 63.7133
    - type: nauc_map_at_5_std
      value: 32.2817
    - type: nauc_map_at_5_diff1
      value: 70.6826
    - type: nauc_map_at_10_max
      value: 63.6566
    - type: nauc_map_at_10_std
      value: 32.2283
    - type: nauc_map_at_10_diff1
      value: 70.8001
    - type: nauc_map_at_20_max
      value: 63.7023
    - type: nauc_map_at_20_std
      value: 32.3021
    - type: nauc_map_at_20_diff1
      value: 70.8584
    - type: nauc_map_at_100_max
      value: 63.645799999999994
    - type: nauc_map_at_100_std
      value: 32.3835
    - type: nauc_map_at_100_diff1
      value: 70.8164
    - type: nauc_map_at_1000_max
      value: 63.6211
    - type: nauc_map_at_1000_std
      value: 32.334
    - type: nauc_map_at_1000_diff1
      value: 70.8146
    - type: nauc_recall_at_1_max
      value: 56.7217
    - type: nauc_recall_at_1_std
      value: 24.8593
    - type: nauc_recall_at_1_diff1
      value: 71.9101
    - type: nauc_recall_at_3_max
      value: 72.6106
    - type: nauc_recall_at_3_std
      value: 38.4448
    - type: nauc_recall_at_3_diff1
      value: 68.58030000000001
    - type: nauc_recall_at_5_max
      value: 78.35889999999999
    - type: nauc_recall_at_5_std
      value: 52.82829999999999
    - type: nauc_recall_at_5_diff1
      value: 69.30239999999999
    - type: nauc_recall_at_10_max
      value: 80.32730000000001
    - type: nauc_recall_at_10_std
      value: 55.5612
    - type: nauc_recall_at_10_diff1
      value: 70.1068
    - type: nauc_recall_at_20_max
      value: 84.4507
    - type: nauc_recall_at_20_std
      value: 62.841100000000004
    - type: nauc_recall_at_20_diff1
      value: 71.2689
    - type: nauc_recall_at_100_max
      value: 86.8251
    - type: nauc_recall_at_100_std
      value: 82.8944
    - type: nauc_recall_at_100_diff1
      value: 67.35950000000001
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 56.7217
    - type: nauc_precision_at_1_std
      value: 24.8593
    - type: nauc_precision_at_1_diff1
      value: 71.9101
    - type: nauc_precision_at_3_max
      value: 72.6106
    - type: nauc_precision_at_3_std
      value: 38.4448
    - type: nauc_precision_at_3_diff1
      value: 68.58030000000001
    - type: nauc_precision_at_5_max
      value: 78.35889999999999
    - type: nauc_precision_at_5_std
      value: 52.82829999999999
    - type: nauc_precision_at_5_diff1
      value: 69.30239999999999
    - type: nauc_precision_at_10_max
      value: 80.32730000000001
    - type: nauc_precision_at_10_std
      value: 55.5612
    - type: nauc_precision_at_10_diff1
      value: 70.1068
    - type: nauc_precision_at_20_max
      value: 84.4507
    - type: nauc_precision_at_20_std
      value: 62.841100000000004
    - type: nauc_precision_at_20_diff1
      value: 71.2689
    - type: nauc_precision_at_100_max
      value: 86.8251
    - type: nauc_precision_at_100_std
      value: 82.8944
    - type: nauc_precision_at_100_diff1
      value: 67.35950000000001
    - type: nauc_precision_at_1000_max
      value: .nan
    - type: nauc_precision_at_1000_std
      value: .nan
    - type: nauc_precision_at_1000_diff1
      value: .nan
    - type: nauc_mrr_at_1_max
      value: 56.7217
    - type: nauc_mrr_at_1_std
      value: 24.8593
    - type: nauc_mrr_at_1_diff1
      value: 71.9101
    - type: nauc_mrr_at_3_max
      value: 63.0821
    - type: nauc_mrr_at_3_std
      value: 30.2166
    - type: nauc_mrr_at_3_diff1
      value: 70.4667
    - type: nauc_mrr_at_5_max
      value: 63.7133
    - type: nauc_mrr_at_5_std
      value: 32.2817
    - type: nauc_mrr_at_5_diff1
      value: 70.6826
    - type: nauc_mrr_at_10_max
      value: 63.6566
    - type: nauc_mrr_at_10_std
      value: 32.2283
    - type: nauc_mrr_at_10_diff1
      value: 70.8001
    - type: nauc_mrr_at_20_max
      value: 63.7023
    - type: nauc_mrr_at_20_std
      value: 32.3021
    - type: nauc_mrr_at_20_diff1
      value: 70.8584
    - type: nauc_mrr_at_100_max
      value: 63.645799999999994
    - type: nauc_mrr_at_100_std
      value: 32.3835
    - type: nauc_mrr_at_100_diff1
      value: 70.8164
    - type: nauc_mrr_at_1000_max
      value: 63.6211
    - type: nauc_mrr_at_1000_std
      value: 32.334
    - type: nauc_mrr_at_1000_diff1
      value: 70.8146
    - type: main_score
      value: 72.83699999999999
    task:
      type: Retrieval
  - dataset:
      config: go
      name: MTEB CodeSearchNetRetrieval (go)
      revision: fdc6a9e39575768c27eb8a2a5f702bf846eb4759
      split: test
      type: code-search-net/code_search_net
    metrics:
    - type: ndcg_at_1
      value: 71.5
    - type: ndcg_at_3
      value: 80.566
    - type: ndcg_at_5
      value: 82.623
    - type: ndcg_at_10
      value: 83.694
    - type: ndcg_at_20
      value: 84.153
    - type: ndcg_at_100
      value: 84.597
    - type: ndcg_at_1000
      value: 84.73
    - type: map_at_1
      value: 71.5
    - type: map_at_3
      value: 78.43299999999999
    - type: map_at_5
      value: 79.57300000000001
    - type: map_at_10
      value: 80.037
    - type: map_at_20
      value: 80.164
    - type: map_at_100
      value: 80.231
    - type: map_at_1000
      value: 80.238
    - type: recall_at_1
      value: 71.5
    - type: recall_at_3
      value: 86.7
    - type: recall_at_5
      value: 91.7
    - type: recall_at_10
      value: 94.89999999999999
    - type: recall_at_20
      value: 96.7
    - type: recall_at_100
      value: 99.0
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 71.5
    - type: precision_at_3
      value: 28.9
    - type: precision_at_5
      value: 18.34
    - type: precision_at_10
      value: 9.49
    - type: precision_at_20
      value: 4.835
    - type: precision_at_100
      value: 0.9900000000000001
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 71.5
    - type: mrr_at_3
      value: 78.43329999999999
    - type: mrr_at_5
      value: 79.5733
    - type: mrr_at_10
      value: 80.0366
    - type: mrr_at_20
      value: 80.164
    - type: mrr_at_100
      value: 80.2314
    - type: mrr_at_1000
      value: 80.2376
    - type: nauc_ndcg_at_1_max
      value: 46.1044
    - type: nauc_ndcg_at_1_std
      value: -4.7079
    - type: nauc_ndcg_at_1_diff1
      value: 75.426
    - type: nauc_ndcg_at_3_max
      value: 52.6854
    - type: nauc_ndcg_at_3_std
      value: -5.7088
    - type: nauc_ndcg_at_3_diff1
      value: 72.5517
    - type: nauc_ndcg_at_5_max
      value: 51.839400000000005
    - type: nauc_ndcg_at_5_std
      value: -6.802700000000001
    - type: nauc_ndcg_at_5_diff1
      value: 72.17710000000001
    - type: nauc_ndcg_at_10_max
      value: 51.4024
    - type: nauc_ndcg_at_10_std
      value: -7.0518
    - type: nauc_ndcg_at_10_diff1
      value: 73.0671
    - type: nauc_ndcg_at_20_max
      value: 51.029
    - type: nauc_ndcg_at_20_std
      value: -6.6751000000000005
    - type: nauc_ndcg_at_20_diff1
      value: 73.4538
    - type: nauc_ndcg_at_100_max
      value: 50.8548
    - type: nauc_ndcg_at_100_std
      value: -5.9427
    - type: nauc_ndcg_at_100_diff1
      value: 73.51950000000001
    - type: nauc_ndcg_at_1000_max
      value: 50.672
    - type: nauc_ndcg_at_1000_std
      value: -6.0391
    - type: nauc_ndcg_at_1000_diff1
      value: 73.5247
    - type: nauc_map_at_1_max
      value: 46.1044
    - type: nauc_map_at_1_std
      value: -4.7079
    - type: nauc_map_at_1_diff1
      value: 75.426
    - type: nauc_map_at_3_max
      value: 50.939299999999996
    - type: nauc_map_at_3_std
      value: -5.3396
    - type: nauc_map_at_3_diff1
      value: 73.42490000000001
    - type: nauc_map_at_5_max
      value: 50.4396
    - type: nauc_map_at_5_std
      value: -5.8186
    - type: nauc_map_at_5_diff1
      value: 73.2819
    - type: nauc_map_at_10_max
      value: 50.27890000000001
    - type: nauc_map_at_10_std
      value: -5.8548
    - type: nauc_map_at_10_diff1
      value: 73.6528
    - type: nauc_map_at_20_max
      value: 50.2054
    - type: nauc_map_at_20_std
      value: -5.7458
    - type: nauc_map_at_20_diff1
      value: 73.7524
    - type: nauc_map_at_100_max
      value: 50.1773
    - type: nauc_map_at_100_std
      value: -5.6738
    - type: nauc_map_at_100_diff1
      value: 73.75460000000001
    - type: nauc_map_at_1000_max
      value: 50.166999999999994
    - type: nauc_map_at_1000_std
      value: -5.6814
    - type: nauc_map_at_1000_diff1
      value: 73.7542
    - type: nauc_recall_at_1_max
      value: 46.1044
    - type: nauc_recall_at_1_std
      value: -4.7079
    - type: nauc_recall_at_1_diff1
      value: 75.426
    - type: nauc_recall_at_3_max
      value: 60.1177
    - type: nauc_recall_at_3_std
      value: -7.3551
    - type: nauc_recall_at_3_diff1
      value: 68.7552
    - type: nauc_recall_at_5_max
      value: 60.249399999999994
    - type: nauc_recall_at_5_std
      value: -13.555600000000002
    - type: nauc_recall_at_5_diff1
      value: 65.0445
    - type: nauc_recall_at_10_max
      value: 61.167
    - type: nauc_recall_at_10_std
      value: -20.4198
    - type: nauc_recall_at_10_diff1
      value: 67.8246
    - type: nauc_recall_at_20_max
      value: 59.404999999999994
    - type: nauc_recall_at_20_std
      value: -21.929399999999998
    - type: nauc_recall_at_20_diff1
      value: 71.1994
    - type: nauc_recall_at_100_max
      value: 66.6713
    - type: nauc_recall_at_100_std
      value: -0.4949
    - type: nauc_recall_at_100_diff1
      value: 72.409
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 46.1044
    - type: nauc_precision_at_1_std
      value: -4.7079
    - type: nauc_precision_at_1_diff1
      value: 75.426
    - type: nauc_precision_at_3_max
      value: 60.1177
    - type: nauc_precision_at_3_std
      value: -7.3551
    - type: nauc_precision_at_3_diff1
      value: 68.7552
    - type: nauc_precision_at_5_max
      value: 60.249399999999994
    - type: nauc_precision_at_5_std
      value: -13.555600000000002
    - type: nauc_precision_at_5_diff1
      value: 65.0445
    - type: nauc_precision_at_10_max
      value: 61.167
    - type: nauc_precision_at_10_std
      value: -20.4198
    - type: nauc_precision_at_10_diff1
      value: 67.8246
    - type: nauc_precision_at_20_max
      value: 59.404999999999994
    - type: nauc_precision_at_20_std
      value: -21.929399999999998
    - type: nauc_precision_at_20_diff1
      value: 71.1994
    - type: nauc_precision_at_100_max
      value: 66.6713
    - type: nauc_precision_at_100_std
      value: -0.4949
    - type: nauc_precision_at_100_diff1
      value: 72.409
    - type: nauc_precision_at_1000_max
      value: .nan
    - type: nauc_precision_at_1000_std
      value: .nan
    - type: nauc_precision_at_1000_diff1
      value: .nan
    - type: nauc_mrr_at_1_max
      value: 46.1044
    - type: nauc_mrr_at_1_std
      value: -4.7079
    - type: nauc_mrr_at_1_diff1
      value: 75.426
    - type: nauc_mrr_at_3_max
      value: 50.939299999999996
    - type: nauc_mrr_at_3_std
      value: -5.3396
    - type: nauc_mrr_at_3_diff1
      value: 73.42490000000001
    - type: nauc_mrr_at_5_max
      value: 50.4396
    - type: nauc_mrr_at_5_std
      value: -5.8186
    - type: nauc_mrr_at_5_diff1
      value: 73.2819
    - type: nauc_mrr_at_10_max
      value: 50.27890000000001
    - type: nauc_mrr_at_10_std
      value: -5.8548
    - type: nauc_mrr_at_10_diff1
      value: 73.6528
    - type: nauc_mrr_at_20_max
      value: 50.2054
    - type: nauc_mrr_at_20_std
      value: -5.7458
    - type: nauc_mrr_at_20_diff1
      value: 73.7524
    - type: nauc_mrr_at_100_max
      value: 50.1773
    - type: nauc_mrr_at_100_std
      value: -5.6738
    - type: nauc_mrr_at_100_diff1
      value: 73.75460000000001
    - type: nauc_mrr_at_1000_max
      value: 50.166999999999994
    - type: nauc_mrr_at_1000_std
      value: -5.6814
    - type: nauc_mrr_at_1000_diff1
      value: 73.7542
    - type: main_score
      value: 83.694
    task:
      type: Retrieval
  - dataset:
      config: ruby
      name: MTEB CodeSearchNetRetrieval (ruby)
      revision: fdc6a9e39575768c27eb8a2a5f702bf846eb4759
      split: test
      type: code-search-net/code_search_net
    metrics:
    - type: ndcg_at_1
      value: 63.1
    - type: ndcg_at_3
      value: 73.48400000000001
    - type: ndcg_at_5
      value: 75.907
    - type: ndcg_at_10
      value: 76.81400000000001
    - type: ndcg_at_20
      value: 77.532
    - type: ndcg_at_100
      value: 78.25800000000001
    - type: ndcg_at_1000
      value: 78.739
    - type: map_at_1
      value: 63.1
    - type: map_at_3
      value: 70.98299999999999
    - type: map_at_5
      value: 72.32300000000001
    - type: map_at_10
      value: 72.7
    - type: map_at_20
      value: 72.902
    - type: map_at_100
      value: 73.00999999999999
    - type: map_at_1000
      value: 73.02499999999999
    - type: recall_at_1
      value: 63.1
    - type: recall_at_3
      value: 80.7
    - type: recall_at_5
      value: 86.6
    - type: recall_at_10
      value: 89.4
    - type: recall_at_20
      value: 92.2
    - type: recall_at_100
      value: 96.0
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 63.1
    - type: precision_at_3
      value: 26.900000000000002
    - type: precision_at_5
      value: 17.32
    - type: precision_at_10
      value: 8.94
    - type: precision_at_20
      value: 4.61
    - type: precision_at_100
      value: 0.96
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 63.1
    - type: mrr_at_3
      value: 70.9833
    - type: mrr_at_5
      value: 72.3233
    - type: mrr_at_10
      value: 72.6995
    - type: mrr_at_20
      value: 72.9017
    - type: mrr_at_100
      value: 73.0097
    - type: mrr_at_1000
      value: 73.0247
    - type: nauc_ndcg_at_1_max
      value: 51.397099999999995
    - type: nauc_ndcg_at_1_std
      value: 5.5686
    - type: nauc_ndcg_at_1_diff1
      value: 67.8159
    - type: nauc_ndcg_at_3_max
      value: 51.7661
    - type: nauc_ndcg_at_3_std
      value: 5.247199999999999
    - type: nauc_ndcg_at_3_diff1
      value: 62.2276
    - type: nauc_ndcg_at_5_max
      value: 52.45649999999999
    - type: nauc_ndcg_at_5_std
      value: 8.3289
    - type: nauc_ndcg_at_5_diff1
      value: 61.5048
    - type: nauc_ndcg_at_10_max
      value: 53.376599999999996
    - type: nauc_ndcg_at_10_std
      value: 10.0975
    - type: nauc_ndcg_at_10_diff1
      value: 61.206
    - type: nauc_ndcg_at_20_max
      value: 53.4219
    - type: nauc_ndcg_at_20_std
      value: 11.3499
    - type: nauc_ndcg_at_20_diff1
      value: 60.670199999999994
    - type: nauc_ndcg_at_100_max
      value: 53.728699999999996
    - type: nauc_ndcg_at_100_std
      value: 11.754299999999999
    - type: nauc_ndcg_at_100_diff1
      value: 61.2795
    - type: nauc_ndcg_at_1000_max
      value: 53.1018
    - type: nauc_ndcg_at_1000_std
      value: 9.7542
    - type: nauc_ndcg_at_1000_diff1
      value: 62.16779999999999
    - type: nauc_map_at_1_max
      value: 51.397099999999995
    - type: nauc_map_at_1_std
      value: 5.5686
    - type: nauc_map_at_1_diff1
      value: 67.8159
    - type: nauc_map_at_3_max
      value: 51.701600000000006
    - type: nauc_map_at_3_std
      value: 5.346900000000001
    - type: nauc_map_at_3_diff1
      value: 63.7526
    - type: nauc_map_at_5_max
      value: 52.05030000000001
    - type: nauc_map_at_5_std
      value: 6.901
    - type: nauc_map_at_5_diff1
      value: 63.4742
    - type: nauc_map_at_10_max
      value: 52.3881
    - type: nauc_map_at_10_std
      value: 7.557899999999999
    - type: nauc_map_at_10_diff1
      value: 63.385000000000005
    - type: nauc_map_at_20_max
      value: 52.3801
    - type: nauc_map_at_20_std
      value: 7.8098
    - type: nauc_map_at_20_diff1
      value: 63.2662
    - type: nauc_map_at_100_max
      value: 52.440799999999996
    - type: nauc_map_at_100_std
      value: 7.8723
    - type: nauc_map_at_100_diff1
      value: 63.362399999999994
    - type: nauc_map_at_1000_max
      value: 52.4276
    - type: nauc_map_at_1000_std
      value: 7.8245
    - type: nauc_map_at_1000_diff1
      value: 63.3886
    - type: nauc_recall_at_1_max
      value: 51.397099999999995
    - type: nauc_recall_at_1_std
      value: 5.5686
    - type: nauc_recall_at_1_diff1
      value: 67.8159
    - type: nauc_recall_at_3_max
      value: 51.995000000000005
    - type: nauc_recall_at_3_std
      value: 4.853
    - type: nauc_recall_at_3_diff1
      value: 56.3023
    - type: nauc_recall_at_5_max
      value: 54.692099999999996
    - type: nauc_recall_at_5_std
      value: 16.4925
    - type: nauc_recall_at_5_diff1
      value: 51.12179999999999
    - type: nauc_recall_at_10_max
      value: 60.454699999999995
    - type: nauc_recall_at_10_std
      value: 28.295900000000003
    - type: nauc_recall_at_10_diff1
      value: 47.063100000000006
    - type: nauc_recall_at_20_max
      value: 63.59740000000001
    - type: nauc_recall_at_20_std
      value: 47.2928
    - type: nauc_recall_at_20_diff1
      value: 37.1627
    - type: nauc_recall_at_100_max
      value: 78.4162
    - type: nauc_recall_at_100_std
      value: 88.6099
    - type: nauc_recall_at_100_diff1
      value: 28.975299999999997
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 51.397099999999995
    - type: nauc_precision_at_1_std
      value: 5.5686
    - type: nauc_precision_at_1_diff1
      value: 67.8159
    - type: nauc_precision_at_3_max
      value: 51.995000000000005
    - type: nauc_precision_at_3_std
      value: 4.853
    - type: nauc_precision_at_3_diff1
      value: 56.3023
    - type: nauc_precision_at_5_max
      value: 54.692099999999996
    - type: nauc_precision_at_5_std
      value: 16.4925
    - type: nauc_precision_at_5_diff1
      value: 51.12179999999999
    - type: nauc_precision_at_10_max
      value: 60.454699999999995
    - type: nauc_precision_at_10_std
      value: 28.295900000000003
    - type: nauc_precision_at_10_diff1
      value: 47.063100000000006
    - type: nauc_precision_at_20_max
      value: 63.59740000000001
    - type: nauc_precision_at_20_std
      value: 47.2928
    - type: nauc_precision_at_20_diff1
      value: 37.1627
    - type: nauc_precision_at_100_max
      value: 78.4162
    - type: nauc_precision_at_100_std
      value: 88.6099
    - type: nauc_precision_at_100_diff1
      value: 28.975299999999997
    - type: nauc_precision_at_1000_max
      value: .nan
    - type: nauc_precision_at_1000_std
      value: .nan
    - type: nauc_precision_at_1000_diff1
      value: .nan
    - type: nauc_mrr_at_1_max
      value: 51.397099999999995
    - type: nauc_mrr_at_1_std
      value: 5.5686
    - type: nauc_mrr_at_1_diff1
      value: 67.8159
    - type: nauc_mrr_at_3_max
      value: 51.701600000000006
    - type: nauc_mrr_at_3_std
      value: 5.346900000000001
    - type: nauc_mrr_at_3_diff1
      value: 63.7526
    - type: nauc_mrr_at_5_max
      value: 52.05030000000001
    - type: nauc_mrr_at_5_std
      value: 6.901
    - type: nauc_mrr_at_5_diff1
      value: 63.4742
    - type: nauc_mrr_at_10_max
      value: 52.3881
    - type: nauc_mrr_at_10_std
      value: 7.557899999999999
    - type: nauc_mrr_at_10_diff1
      value: 63.385000000000005
    - type: nauc_mrr_at_20_max
      value: 52.3801
    - type: nauc_mrr_at_20_std
      value: 7.8098
    - type: nauc_mrr_at_20_diff1
      value: 63.2662
    - type: nauc_mrr_at_100_max
      value: 52.440799999999996
    - type: nauc_mrr_at_100_std
      value: 7.8723
    - type: nauc_mrr_at_100_diff1
      value: 63.362399999999994
    - type: nauc_mrr_at_1000_max
      value: 52.4276
    - type: nauc_mrr_at_1000_std
      value: 7.8245
    - type: nauc_mrr_at_1000_diff1
      value: 63.3886
    - type: main_score
      value: 76.81400000000001
    task:
      type: Retrieval
  - dataset:
      config: java
      name: MTEB CodeSearchNetRetrieval (java)
      revision: fdc6a9e39575768c27eb8a2a5f702bf846eb4759
      split: test
      type: code-search-net/code_search_net
    metrics:
    - type: ndcg_at_1
      value: 52.1
    - type: ndcg_at_3
      value: 64.248
    - type: ndcg_at_5
      value: 67.213
    - type: ndcg_at_10
      value: 69.41199999999999
    - type: ndcg_at_20
      value: 70.43700000000001
    - type: ndcg_at_100
      value: 71.33800000000001
    - type: ndcg_at_1000
      value: 71.887
    - type: map_at_1
      value: 52.1
    - type: map_at_3
      value: 61.35
    - type: map_at_5
      value: 62.995000000000005
    - type: map_at_10
      value: 63.92
    - type: map_at_20
      value: 64.209
    - type: map_at_100
      value: 64.338
    - type: map_at_1000
      value: 64.352
    - type: recall_at_1
      value: 52.1
    - type: recall_at_3
      value: 72.6
    - type: recall_at_5
      value: 79.80000000000001
    - type: recall_at_10
      value: 86.5
    - type: recall_at_20
      value: 90.5
    - type: recall_at_100
      value: 95.3
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 52.1
    - type: precision_at_3
      value: 24.2
    - type: precision_at_5
      value: 15.959999999999999
    - type: precision_at_10
      value: 8.649999999999999
    - type: precision_at_20
      value: 4.5249999999999995
    - type: precision_at_100
      value: 0.9530000000000001
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 52.1
    - type: mrr_at_3
      value: 61.35
    - type: mrr_at_5
      value: 62.995000000000005
    - type: mrr_at_10
      value: 63.9199
    - type: mrr_at_20
      value: 64.209
    - type: mrr_at_100
      value: 64.338
    - type: mrr_at_1000
      value: 64.352
    - type: nauc_ndcg_at_1_max
      value: 35.1263
    - type: nauc_ndcg_at_1_std
      value: -12.454600000000001
    - type: nauc_ndcg_at_1_diff1
      value: 58.824
    - type: nauc_ndcg_at_3_max
      value: 40.6703
    - type: nauc_ndcg_at_3_std
      value: -9.0987
    - type: nauc_ndcg_at_3_diff1
      value: 52.3502
    - type: nauc_ndcg_at_5_max
      value: 41.3895
    - type: nauc_ndcg_at_5_std
      value: -7.630199999999999
    - type: nauc_ndcg_at_5_diff1
      value: 51.614599999999996
    - type: nauc_ndcg_at_10_max
      value: 42.345699999999994
    - type: nauc_ndcg_at_10_std
      value: -5.084700000000001
    - type: nauc_ndcg_at_10_diff1
      value: 53.396
    - type: nauc_ndcg_at_20_max
      value: 42.215399999999995
    - type: nauc_ndcg_at_20_std
      value: -4.825
    - type: nauc_ndcg_at_20_diff1
      value: 53.296699999999994
    - type: nauc_ndcg_at_100_max
      value: 42.0653
    - type: nauc_ndcg_at_100_std
      value: -4.356
    - type: nauc_ndcg_at_100_diff1
      value: 53.595099999999995
    - type: nauc_ndcg_at_1000_max
      value: 41.016200000000005
    - type: nauc_ndcg_at_1000_std
      value: -6.2975
    - type: nauc_ndcg_at_1000_diff1
      value: 53.7728
    - type: nauc_map_at_1_max
      value: 35.1263
    - type: nauc_map_at_1_std
      value: -12.454600000000001
    - type: nauc_map_at_1_diff1
      value: 58.824
    - type: nauc_map_at_3_max
      value: 38.9371
    - type: nauc_map_at_3_std
      value: -10.1381
    - type: nauc_map_at_3_diff1
      value: 54.008500000000005
    - type: nauc_map_at_5_max
      value: 39.1816
    - type: nauc_map_at_5_std
      value: -9.4667
    - type: nauc_map_at_5_diff1
      value: 53.748
    - type: nauc_map_at_10_max
      value: 39.5398
    - type: nauc_map_at_10_std
      value: -8.5131
    - type: nauc_map_at_10_diff1
      value: 54.433699999999995
    - type: nauc_map_at_20_max
      value: 39.4926
    - type: nauc_map_at_20_std
      value: -8.4859
    - type: nauc_map_at_20_diff1
      value: 54.4071
    - type: nauc_map_at_100_max
      value: 39.4716
    - type: nauc_map_at_100_std
      value: -8.4321
    - type: nauc_map_at_100_diff1
      value: 54.4382
    - type: nauc_map_at_1000_max
      value: 39.4529
    - type: nauc_map_at_1000_std
      value: -8.468499999999999
    - type: nauc_map_at_1000_diff1
      value: 54.4425
    - type: nauc_recall_at_1_max
      value: 35.1263
    - type: nauc_recall_at_1_std
      value: -12.454600000000001
    - type: nauc_recall_at_1_diff1
      value: 58.824
    - type: nauc_recall_at_3_max
      value: 46.9678
    - type: nauc_recall_at_3_std
      value: -5.3263
    - type: nauc_recall_at_3_diff1
      value: 46.4906
    - type: nauc_recall_at_5_max
      value: 51.4392
    - type: nauc_recall_at_5_std
      value: 0.864
    - type: nauc_recall_at_5_diff1
      value: 42.1144
    - type: nauc_recall_at_10_max
      value: 60.5469
    - type: nauc_recall_at_10_std
      value: 18.2879
    - type: nauc_recall_at_10_diff1
      value: 48.3112
    - type: nauc_recall_at_20_max
      value: 65.8794
    - type: nauc_recall_at_20_std
      value: 29.569499999999998
    - type: nauc_recall_at_20_diff1
      value: 45.7507
    - type: nauc_recall_at_100_max
      value: 85.5603
    - type: nauc_recall_at_100_std
      value: 75.366
    - type: nauc_recall_at_100_diff1
      value: 46.4102
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 35.1263
    - type: nauc_precision_at_1_std
      value: -12.454600000000001
    - type: nauc_precision_at_1_diff1
      value: 58.824
    - type: nauc_precision_at_3_max
      value: 46.9678
    - type: nauc_precision_at_3_std
      value: -5.3263
    - type: nauc_precision_at_3_diff1
      value: 46.4906
    - type: nauc_precision_at_5_max
      value: 51.4392
    - type: nauc_precision_at_5_std
      value: 0.864
    - type: nauc_precision_at_5_diff1
      value: 42.1144
    - type: nauc_precision_at_10_max
      value: 60.5469
    - type: nauc_precision_at_10_std
      value: 18.2879
    - type: nauc_precision_at_10_diff1
      value: 48.3112
    - type: nauc_precision_at_20_max
      value: 65.8794
    - type: nauc_precision_at_20_std
      value: 29.569499999999998
    - type: nauc_precision_at_20_diff1
      value: 45.7507
    - type: nauc_precision_at_100_max
      value: 85.5603
    - type: nauc_precision_at_100_std
      value: 75.366
    - type: nauc_precision_at_100_diff1
      value: 46.4102
    - type: nauc_precision_at_1000_max
      value: .nan
    - type: nauc_precision_at_1000_std
      value: .nan
    - type: nauc_precision_at_1000_diff1
      value: .nan
    - type: nauc_mrr_at_1_max
      value: 35.1263
    - type: nauc_mrr_at_1_std
      value: -12.454600000000001
    - type: nauc_mrr_at_1_diff1
      value: 58.824
    - type: nauc_mrr_at_3_max
      value: 38.9371
    - type: nauc_mrr_at_3_std
      value: -10.1381
    - type: nauc_mrr_at_3_diff1
      value: 54.008500000000005
    - type: nauc_mrr_at_5_max
      value: 39.1816
    - type: nauc_mrr_at_5_std
      value: -9.4667
    - type: nauc_mrr_at_5_diff1
      value: 53.748
    - type: nauc_mrr_at_10_max
      value: 39.5398
    - type: nauc_mrr_at_10_std
      value: -8.5131
    - type: nauc_mrr_at_10_diff1
      value: 54.433699999999995
    - type: nauc_mrr_at_20_max
      value: 39.4926
    - type: nauc_mrr_at_20_std
      value: -8.4859
    - type: nauc_mrr_at_20_diff1
      value: 54.4071
    - type: nauc_mrr_at_100_max
      value: 39.4716
    - type: nauc_mrr_at_100_std
      value: -8.4321
    - type: nauc_mrr_at_100_diff1
      value: 54.4382
    - type: nauc_mrr_at_1000_max
      value: 39.4529
    - type: nauc_mrr_at_1000_std
      value: -8.468499999999999
    - type: nauc_mrr_at_1000_diff1
      value: 54.4425
    - type: main_score
      value: 69.41199999999999
    task:
      type: Retrieval
  - dataset:
      config: php
      name: MTEB CodeSearchNetRetrieval (php)
      revision: fdc6a9e39575768c27eb8a2a5f702bf846eb4759
      split: test
      type: code-search-net/code_search_net
    metrics:
    - type: ndcg_at_1
      value: 60.3
    - type: ndcg_at_3
      value: 71.487
    - type: ndcg_at_5
      value: 73.359
    - type: ndcg_at_10
      value: 75.13
    - type: ndcg_at_20
      value: 75.768
    - type: ndcg_at_100
      value: 76.652
    - type: ndcg_at_1000
      value: 77.061
    - type: map_at_1
      value: 60.3
    - type: map_at_3
      value: 68.75
    - type: map_at_5
      value: 69.8
    - type: map_at_10
      value: 70.526
    - type: map_at_20
      value: 70.705
    - type: map_at_100
      value: 70.838
    - type: map_at_1000
      value: 70.84899999999999
    - type: recall_at_1
      value: 60.3
    - type: recall_at_3
      value: 79.4
    - type: recall_at_5
      value: 83.89999999999999
    - type: recall_at_10
      value: 89.4
    - type: recall_at_20
      value: 91.9
    - type: recall_at_100
      value: 96.5
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 60.3
    - type: precision_at_3
      value: 26.467000000000002
    - type: precision_at_5
      value: 16.78
    - type: precision_at_10
      value: 8.94
    - type: precision_at_20
      value: 4.595
    - type: precision_at_100
      value: 0.9650000000000001
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 60.3
    - type: mrr_at_3
      value: 68.75
    - type: mrr_at_5
      value: 69.8
    - type: mrr_at_10
      value: 70.52619999999999
    - type: mrr_at_20
      value: 70.7048
    - type: mrr_at_100
      value: 70.838
    - type: mrr_at_1000
      value: 70.8488
    - type: nauc_ndcg_at_1_max
      value: 45.8593
    - type: nauc_ndcg_at_1_std
      value: 13.2893
    - type: nauc_ndcg_at_1_diff1
      value: 66.718
    - type: nauc_ndcg_at_3_max
      value: 55.4137
    - type: nauc_ndcg_at_3_std
      value: 23.0079
    - type: nauc_ndcg_at_3_diff1
      value: 63.693200000000004
    - type: nauc_ndcg_at_5_max
      value: 56.2033
    - type: nauc_ndcg_at_5_std
      value: 25.2245
    - type: nauc_ndcg_at_5_diff1
      value: 65.0071
    - type: nauc_ndcg_at_10_max
      value: 56.540400000000005
    - type: nauc_ndcg_at_10_std
      value: 26.323400000000003
    - type: nauc_ndcg_at_10_diff1
      value: 65.8486
    - type: nauc_ndcg_at_20_max
      value: 56.2864
    - type: nauc_ndcg_at_20_std
      value: 26.6575
    - type: nauc_ndcg_at_20_diff1
      value: 65.6045
    - type: nauc_ndcg_at_100_max
      value: 55.2604
    - type: nauc_ndcg_at_100_std
      value: 24.9411
    - type: nauc_ndcg_at_100_diff1
      value: 65.9764
    - type: nauc_ndcg_at_1000_max
      value: 54.514799999999994
    - type: nauc_ndcg_at_1000_std
      value: 23.7436
    - type: nauc_ndcg_at_1000_diff1
      value: 65.6415
    - type: nauc_map_at_1_max
      value: 45.8593
    - type: nauc_map_at_1_std
      value: 13.2893
    - type: nauc_map_at_1_diff1
      value: 66.718
    - type: nauc_map_at_3_max
      value: 52.809799999999996
    - type: nauc_map_at_3_std
      value: 20.2338
    - type: nauc_map_at_3_diff1
      value: 64.4615
    - type: nauc_map_at_5_max
      value: 53.10080000000001
    - type: nauc_map_at_5_std
      value: 21.2375
    - type: nauc_map_at_5_diff1
      value: 65.1416
    - type: nauc_map_at_10_max
      value: 53.117000000000004
    - type: nauc_map_at_10_std
      value: 21.512999999999998
    - type: nauc_map_at_10_diff1
      value: 65.4616
    - type: nauc_map_at_20_max
      value: 53.0434
    - type: nauc_map_at_20_std
      value: 21.5865
    - type: nauc_map_at_20_diff1
      value: 65.4014
    - type: nauc_map_at_100_max
      value: 52.898199999999996
    - type: nauc_map_at_100_std
      value: 21.357
    - type: nauc_map_at_100_diff1
      value: 65.4438
    - type: nauc_map_at_1000_max
      value: 52.8844
    - type: nauc_map_at_1000_std
      value: 21.3357
    - type: nauc_map_at_1000_diff1
      value: 65.4388
    - type: nauc_recall_at_1_max
      value: 45.8593
    - type: nauc_recall_at_1_std
      value: 13.2893
    - type: nauc_recall_at_1_diff1
      value: 66.718
    - type: nauc_recall_at_3_max
      value: 65.5352
    - type: nauc_recall_at_3_std
      value: 33.8655
    - type: nauc_recall_at_3_diff1
      value: 60.740300000000005
    - type: nauc_recall_at_5_max
      value: 70.9819
    - type: nauc_recall_at_5_std
      value: 44.5937
    - type: nauc_recall_at_5_diff1
      value: 64.7568
    - type: nauc_recall_at_10_max
      value: 80.07469999999999
    - type: nauc_recall_at_10_std
      value: 60.3717
    - type: nauc_recall_at_10_diff1
      value: 69.6608
    - type: nauc_recall_at_20_max
      value: 84.3633
    - type: nauc_recall_at_20_std
      value: 73.2136
    - type: nauc_recall_at_20_diff1
      value: 68.3675
    - type: nauc_recall_at_100_max
      value: 91.4499
    - type: nauc_recall_at_100_std
      value: 83.50410000000001
    - type: nauc_recall_at_100_diff1
      value: 82.91579999999999
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 45.8593
    - type: nauc_precision_at_1_std
      value: 13.2893
    - type: nauc_precision_at_1_diff1
      value: 66.718
    - type: nauc_precision_at_3_max
      value: 65.5352
    - type: nauc_precision_at_3_std
      value: 33.8655
    - type: nauc_precision_at_3_diff1
      value: 60.740300000000005
    - type: nauc_precision_at_5_max
      value: 70.9819
    - type: nauc_precision_at_5_std
      value: 44.5937
    - type: nauc_precision_at_5_diff1
      value: 64.7568
    - type: nauc_precision_at_10_max
      value: 80.07469999999999
    - type: nauc_precision_at_10_std
      value: 60.3717
    - type: nauc_precision_at_10_diff1
      value: 69.6608
    - type: nauc_precision_at_20_max
      value: 84.3633
    - type: nauc_precision_at_20_std
      value: 73.2136
    - type: nauc_precision_at_20_diff1
      value: 68.3675
    - type: nauc_precision_at_100_max
      value: 91.4499
    - type: nauc_precision_at_100_std
      value: 83.50410000000001
    - type: nauc_precision_at_100_diff1
      value: 82.91579999999999
    - type: nauc_precision_at_1000_max
      value: .nan
    - type: nauc_precision_at_1000_std
      value: .nan
    - type: nauc_precision_at_1000_diff1
      value: .nan
    - type: nauc_mrr_at_1_max
      value: 45.8593
    - type: nauc_mrr_at_1_std
      value: 13.2893
    - type: nauc_mrr_at_1_diff1
      value: 66.718
    - type: nauc_mrr_at_3_max
      value: 52.809799999999996
    - type: nauc_mrr_at_3_std
      value: 20.2338
    - type: nauc_mrr_at_3_diff1
      value: 64.4615
    - type: nauc_mrr_at_5_max
      value: 53.10080000000001
    - type: nauc_mrr_at_5_std
      value: 21.2375
    - type: nauc_mrr_at_5_diff1
      value: 65.1416
    - type: nauc_mrr_at_10_max
      value: 53.117000000000004
    - type: nauc_mrr_at_10_std
      value: 21.512999999999998
    - type: nauc_mrr_at_10_diff1
      value: 65.4616
    - type: nauc_mrr_at_20_max
      value: 53.0434
    - type: nauc_mrr_at_20_std
      value: 21.5865
    - type: nauc_mrr_at_20_diff1
      value: 65.4014
    - type: nauc_mrr_at_100_max
      value: 52.898199999999996
    - type: nauc_mrr_at_100_std
      value: 21.357
    - type: nauc_mrr_at_100_diff1
      value: 65.4438
    - type: nauc_mrr_at_1000_max
      value: 52.8844
    - type: nauc_mrr_at_1000_std
      value: 21.3357
    - type: nauc_mrr_at_1000_diff1
      value: 65.4388
    - type: main_score
      value: 75.13
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CodeTransOceanContest (default)
      revision: 20da4eb20a4b17300c0986ee148c90867a7f2a4d
      split: test
      type: CoIR-Retrieval/codetrans-contest
    metrics:
    - type: ndcg_at_1
      value: 55.656000000000006
    - type: ndcg_at_3
      value: 62.497
    - type: ndcg_at_5
      value: 64.95100000000001
    - type: ndcg_at_10
      value: 66.733
    - type: ndcg_at_20
      value: 67.778
    - type: ndcg_at_100
      value: 69.962
    - type: ndcg_at_1000
      value: 70.736
    - type: map_at_1
      value: 55.656000000000006
    - type: map_at_3
      value: 60.934999999999995
    - type: map_at_5
      value: 62.315
    - type: map_at_10
      value: 63.065000000000005
    - type: map_at_20
      value: 63.36000000000001
    - type: map_at_100
      value: 63.663000000000004
    - type: map_at_1000
      value: 63.696
    - type: recall_at_1
      value: 55.656000000000006
    - type: recall_at_3
      value: 66.968
    - type: recall_at_5
      value: 72.851
    - type: recall_at_10
      value: 78.281
    - type: recall_at_20
      value: 82.353
    - type: recall_at_100
      value: 94.118
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 55.656000000000006
    - type: precision_at_3
      value: 22.323
    - type: precision_at_5
      value: 14.57
    - type: precision_at_10
      value: 7.828
    - type: precision_at_20
      value: 4.118
    - type: precision_at_100
      value: 0.941
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 55.656099999999995
    - type: mrr_at_3
      value: 60.9351
    - type: mrr_at_5
      value: 62.315200000000004
    - type: mrr_at_10
      value: 63.0653
    - type: mrr_at_20
      value: 63.360099999999996
    - type: mrr_at_100
      value: 63.6629
    - type: mrr_at_1000
      value: 63.695800000000006
    - type: nauc_ndcg_at_1_max
      value: 51.957600000000006
    - type: nauc_ndcg_at_1_std
      value: -1.4414
    - type: nauc_ndcg_at_1_diff1
      value: 73.7269
    - type: nauc_ndcg_at_3_max
      value: 56.2033
    - type: nauc_ndcg_at_3_std
      value: -0.5342
    - type: nauc_ndcg_at_3_diff1
      value: 71.29339999999999
    - type: nauc_ndcg_at_5_max
      value: 53.2043
    - type: nauc_ndcg_at_5_std
      value: -4.2406
    - type: nauc_ndcg_at_5_diff1
      value: 71.288
    - type: nauc_ndcg_at_10_max
      value: 53.864999999999995
    - type: nauc_ndcg_at_10_std
      value: -1.7964
    - type: nauc_ndcg_at_10_diff1
      value: 71.3515
    - type: nauc_ndcg_at_20_max
      value: 53.8995
    - type: nauc_ndcg_at_20_std
      value: -2.3122
    - type: nauc_ndcg_at_20_diff1
      value: 71.5024
    - type: nauc_ndcg_at_100_max
      value: 53.7574
    - type: nauc_ndcg_at_100_std
      value: -2.1357
    - type: nauc_ndcg_at_100_diff1
      value: 71.57249999999999
    - type: nauc_ndcg_at_1000_max
      value: 53.7629
    - type: nauc_ndcg_at_1000_std
      value: -2.2336
    - type: nauc_ndcg_at_1000_diff1
      value: 71.6512
    - type: nauc_map_at_1_max
      value: 51.957600000000006
    - type: nauc_map_at_1_std
      value: -1.4414
    - type: nauc_map_at_1_diff1
      value: 73.7269
    - type: nauc_map_at_3_max
      value: 55.3725
    - type: nauc_map_at_3_std
      value: -0.7385
    - type: nauc_map_at_3_diff1
      value: 71.94669999999999
    - type: nauc_map_at_5_max
      value: 53.759100000000004
    - type: nauc_map_at_5_std
      value: -2.6806
    - type: nauc_map_at_5_diff1
      value: 71.97
    - type: nauc_map_at_10_max
      value: 53.9832
    - type: nauc_map_at_10_std
      value: -1.8215
    - type: nauc_map_at_10_diff1
      value: 72.0873
    - type: nauc_map_at_20_max
      value: 53.9655
    - type: nauc_map_at_20_std
      value: -1.9612
    - type: nauc_map_at_20_diff1
      value: 72.1207
    - type: nauc_map_at_100_max
      value: 53.8791
    - type: nauc_map_at_100_std
      value: -1.9848000000000001
    - type: nauc_map_at_100_diff1
      value: 72.0929
    - type: nauc_map_at_1000_max
      value: 53.8818
    - type: nauc_map_at_1000_std
      value: -1.9868000000000001
    - type: nauc_map_at_1000_diff1
      value: 72.0883
    - type: nauc_recall_at_1_max
      value: 51.957600000000006
    - type: nauc_recall_at_1_std
      value: -1.4414
    - type: nauc_recall_at_1_diff1
      value: 73.7269
    - type: nauc_recall_at_3_max
      value: 58.7272
    - type: nauc_recall_at_3_std
      value: 0.10269999999999999
    - type: nauc_recall_at_3_diff1
      value: 69.2012
    - type: nauc_recall_at_5_max
      value: 50.545700000000004
    - type: nauc_recall_at_5_std
      value: -10.5393
    - type: nauc_recall_at_5_diff1
      value: 68.8226
    - type: nauc_recall_at_10_max
      value: 53.0698
    - type: nauc_recall_at_10_std
      value: -0.7827000000000001
    - type: nauc_recall_at_10_diff1
      value: 68.00110000000001
    - type: nauc_recall_at_20_max
      value: 53.4631
    - type: nauc_recall_at_20_std
      value: -3.6452
    - type: nauc_recall_at_20_diff1
      value: 68.3947
    - type: nauc_recall_at_100_max
      value: 54.212700000000005
    - type: nauc_recall_at_100_std
      value: 1.2398
    - type: nauc_recall_at_100_diff1
      value: 67.33590000000001
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 51.957600000000006
    - type: nauc_precision_at_1_std
      value: -1.4414
    - type: nauc_precision_at_1_diff1
      value: 73.7269
    - type: nauc_precision_at_3_max
      value: 58.7272
    - type: nauc_precision_at_3_std
      value: 0.10269999999999999
    - type: nauc_precision_at_3_diff1
      value: 69.2012
    - type: nauc_precision_at_5_max
      value: 50.545700000000004
    - type: nauc_precision_at_5_std
      value: -10.5393
    - type: nauc_precision_at_5_diff1
      value: 68.8226
    - type: nauc_precision_at_10_max
      value: 53.0698
    - type: nauc_precision_at_10_std
      value: -0.7827000000000001
    - type: nauc_precision_at_10_diff1
      value: 68.00110000000001
    - type: nauc_precision_at_20_max
      value: 53.4631
    - type: nauc_precision_at_20_std
      value: -3.6452
    - type: nauc_precision_at_20_diff1
      value: 68.3947
    - type: nauc_precision_at_100_max
      value: 54.212700000000005
    - type: nauc_precision_at_100_std
      value: 1.2398
    - type: nauc_precision_at_100_diff1
      value: 67.33590000000001
    - type: nauc_precision_at_1000_max
      value: 100.0
    - type: nauc_precision_at_1000_std
      value: 100.0
    - type: nauc_precision_at_1000_diff1
      value: 100.0
    - type: nauc_mrr_at_1_max
      value: 51.957600000000006
    - type: nauc_mrr_at_1_std
      value: -1.4414
    - type: nauc_mrr_at_1_diff1
      value: 73.7269
    - type: nauc_mrr_at_3_max
      value: 55.3725
    - type: nauc_mrr_at_3_std
      value: -0.7385
    - type: nauc_mrr_at_3_diff1
      value: 71.94669999999999
    - type: nauc_mrr_at_5_max
      value: 53.759100000000004
    - type: nauc_mrr_at_5_std
      value: -2.6806
    - type: nauc_mrr_at_5_diff1
      value: 71.97
    - type: nauc_mrr_at_10_max
      value: 53.9832
    - type: nauc_mrr_at_10_std
      value: -1.8215
    - type: nauc_mrr_at_10_diff1
      value: 72.0873
    - type: nauc_mrr_at_20_max
      value: 53.9655
    - type: nauc_mrr_at_20_std
      value: -1.9612
    - type: nauc_mrr_at_20_diff1
      value: 72.1207
    - type: nauc_mrr_at_100_max
      value: 53.8791
    - type: nauc_mrr_at_100_std
      value: -1.9848000000000001
    - type: nauc_mrr_at_100_diff1
      value: 72.0929
    - type: nauc_mrr_at_1000_max
      value: 53.8818
    - type: nauc_mrr_at_1000_std
      value: -1.9868000000000001
    - type: nauc_mrr_at_1000_diff1
      value: 72.0883
    - type: main_score
      value: 66.733
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CodeTransOceanDL (default)
      revision: 281562cb8a1265ab5c0824bfa6ddcd9b0a15618f
      split: test
      type: CoIR-Retrieval/codetrans-dl
    metrics:
    - type: ndcg_at_1
      value: 8.889
    - type: ndcg_at_3
      value: 9.868
    - type: ndcg_at_5
      value: 16.543
    - type: ndcg_at_10
      value: 29.599999999999998
    - type: ndcg_at_20
      value: 36.004999999999995
    - type: ndcg_at_100
      value: 37.442
    - type: ndcg_at_1000
      value: 37.601
    - type: map_at_1
      value: 8.889
    - type: map_at_3
      value: 9.629999999999999
    - type: map_at_5
      value: 13.491
    - type: map_at_10
      value: 18.733
    - type: map_at_20
      value: 20.687
    - type: map_at_100
      value: 20.886
    - type: map_at_1000
      value: 20.895
    - type: recall_at_1
      value: 8.889
    - type: recall_at_3
      value: 10.556000000000001
    - type: recall_at_5
      value: 26.111
    - type: recall_at_10
      value: 67.22200000000001
    - type: recall_at_20
      value: 91.111
    - type: recall_at_100
      value: 98.88900000000001
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 8.889
    - type: precision_at_3
      value: 3.519
    - type: precision_at_5
      value: 5.222
    - type: precision_at_10
      value: 6.722
    - type: precision_at_20
      value: 4.556
    - type: precision_at_100
      value: 0.989
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 1.6667
    - type: mrr_at_3
      value: 7.963000000000001
    - type: mrr_at_5
      value: 9.6296
    - type: mrr_at_10
      value: 15.607099999999999
    - type: mrr_at_20
      value: 17.2877
    - type: mrr_at_100
      value: 17.5377
    - type: mrr_at_1000
      value: 17.5465
    - type: nauc_ndcg_at_1_max
      value: -41.348600000000005
    - type: nauc_ndcg_at_1_std
      value: -29.3584
    - type: nauc_ndcg_at_1_diff1
      value: -31.9493
    - type: nauc_ndcg_at_3_max
      value: -42.877700000000004
    - type: nauc_ndcg_at_3_std
      value: -31.703599999999998
    - type: nauc_ndcg_at_3_diff1
      value: -26.914500000000004
    - type: nauc_ndcg_at_5_max
      value: -33.1784
    - type: nauc_ndcg_at_5_std
      value: -24.2625
    - type: nauc_ndcg_at_5_diff1
      value: -11.164399999999999
    - type: nauc_ndcg_at_10_max
      value: -34.5597
    - type: nauc_ndcg_at_10_std
      value: -28.0239
    - type: nauc_ndcg_at_10_diff1
      value: -8.6589
    - type: nauc_ndcg_at_20_max
      value: -41.0648
    - type: nauc_ndcg_at_20_std
      value: -28.6854
    - type: nauc_ndcg_at_20_diff1
      value: -12.1999
    - type: nauc_ndcg_at_100_max
      value: -38.2277
    - type: nauc_ndcg_at_100_std
      value: -30.397999999999996
    - type: nauc_ndcg_at_100_diff1
      value: -14.3859
    - type: nauc_ndcg_at_1000_max
      value: -38.6002
    - type: nauc_ndcg_at_1000_std
      value: -28.9056
    - type: nauc_ndcg_at_1000_diff1
      value: -14.619499999999999
    - type: nauc_map_at_1_max
      value: -41.348600000000005
    - type: nauc_map_at_1_std
      value: -29.3584
    - type: nauc_map_at_1_diff1
      value: -31.9493
    - type: nauc_map_at_3_max
      value: -42.5041
    - type: nauc_map_at_3_std
      value: -31.1456
    - type: nauc_map_at_3_diff1
      value: -27.8752
    - type: nauc_map_at_5_max
      value: -36.146
    - type: nauc_map_at_5_std
      value: -26.268900000000002
    - type: nauc_map_at_5_diff1
      value: -17.1717
    - type: nauc_map_at_10_max
      value: -36.594300000000004
    - type: nauc_map_at_10_std
      value: -27.884199999999996
    - type: nauc_map_at_10_diff1
      value: -15.7719
    - type: nauc_map_at_20_max
      value: -38.9209
    - type: nauc_map_at_20_std
      value: -28.2712
    - type: nauc_map_at_20_diff1
      value: -17.167199999999998
    - type: nauc_map_at_100_max
      value: -38.5835
    - type: nauc_map_at_100_std
      value: -28.5457
    - type: nauc_map_at_100_diff1
      value: -17.4205
    - type: nauc_map_at_1000_max
      value: -38.6011
    - type: nauc_map_at_1000_std
      value: -28.4752
    - type: nauc_map_at_1000_diff1
      value: -17.4332
    - type: nauc_recall_at_1_max
      value: -41.348600000000005
    - type: nauc_recall_at_1_std
      value: -29.3584
    - type: nauc_recall_at_1_diff1
      value: -31.9493
    - type: nauc_recall_at_3_max
      value: -43.884499999999996
    - type: nauc_recall_at_3_std
      value: -33.202
    - type: nauc_recall_at_3_diff1
      value: -24.4202
    - type: nauc_recall_at_5_max
      value: -27.2488
    - type: nauc_recall_at_5_std
      value: -20.238999999999997
    - type: nauc_recall_at_5_diff1
      value: 0.5009
    - type: nauc_recall_at_10_max
      value: -30.416700000000002
    - type: nauc_recall_at_10_std
      value: -29.2207
    - type: nauc_recall_at_10_diff1
      value: 7.2459
    - type: nauc_recall_at_20_max
      value: -63.0894
    - type: nauc_recall_at_20_std
      value: -33.3975
    - type: nauc_recall_at_20_diff1
      value: 12.6371
    - type: nauc_recall_at_100_max
      value: -2.4276
    - type: nauc_recall_at_100_std
      value: -173.9963
    - type: nauc_recall_at_100_diff1
      value: 7.9365000000000006
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: -41.348600000000005
    - type: nauc_precision_at_1_std
      value: -29.3584
    - type: nauc_precision_at_1_diff1
      value: -31.9493
    - type: nauc_precision_at_3_max
      value: -43.884499999999996
    - type: nauc_precision_at_3_std
      value: -33.202
    - type: nauc_precision_at_3_diff1
      value: -24.4202
    - type: nauc_precision_at_5_max
      value: -27.2488
    - type: nauc_precision_at_5_std
      value: -20.238999999999997
    - type: nauc_precision_at_5_diff1
      value: 0.5009
    - type: nauc_precision_at_10_max
      value: -30.416700000000002
    - type: nauc_precision_at_10_std
      value: -29.2207
    - type: nauc_precision_at_10_diff1
      value: 7.2459
    - type: nauc_precision_at_20_max
      value: -63.0894
    - type: nauc_precision_at_20_std
      value: -33.3975
    - type: nauc_precision_at_20_diff1
      value: 12.6371
    - type: nauc_precision_at_100_max
      value: -2.4276
    - type: nauc_precision_at_100_std
      value: -173.9963
    - type: nauc_precision_at_100_diff1
      value: 7.9365000000000006
    - type: nauc_precision_at_1000_max
      value: 100.0
    - type: nauc_precision_at_1000_std
      value: 100.0
    - type: nauc_precision_at_1000_diff1
      value: 100.0
    - type: nauc_mrr_at_1_max
      value: -54.9682
    - type: nauc_mrr_at_1_std
      value: -52.464
    - type: nauc_mrr_at_1_diff1
      value: -14.193700000000002
    - type: nauc_mrr_at_3_max
      value: -26.9762
    - type: nauc_mrr_at_3_std
      value: -21.9893
    - type: nauc_mrr_at_3_diff1
      value: 22.9584
    - type: nauc_mrr_at_5_max
      value: -26.8118
    - type: nauc_mrr_at_5_std
      value: -25.476300000000002
    - type: nauc_mrr_at_5_diff1
      value: 16.8933
    - type: nauc_mrr_at_10_max
      value: -32.9675
    - type: nauc_mrr_at_10_std
      value: -29.8253
    - type: nauc_mrr_at_10_diff1
      value: 23.7632
    - type: nauc_mrr_at_20_max
      value: -32.831700000000005
    - type: nauc_mrr_at_20_std
      value: -27.0541
    - type: nauc_mrr_at_20_diff1
      value: 21.238599999999998
    - type: nauc_mrr_at_100_max
      value: -32.2085
    - type: nauc_mrr_at_100_std
      value: -27.3913
    - type: nauc_mrr_at_100_diff1
      value: 21.2347
    - type: nauc_mrr_at_1000_max
      value: -32.230399999999996
    - type: nauc_mrr_at_1000_std
      value: -27.2842
    - type: nauc_mrr_at_1000_diff1
      value: 21.2439
    - type: main_score
      value: 29.599999999999998
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB CosQA (default)
      revision: bc5efb7e9d437246ce393ed19d772e08e4a79535
      split: test
      type: CoIR-Retrieval/cosqa
    metrics:
    - type: ndcg_at_1
      value: 16.0
    - type: ndcg_at_3
      value: 25.474000000000004
    - type: ndcg_at_5
      value: 31.291000000000004
    - type: ndcg_at_10
      value: 36.619
    - type: ndcg_at_20
      value: 39.513999999999996
    - type: ndcg_at_100
      value: 43.002
    - type: ndcg_at_1000
      value: 43.846000000000004
    - type: map_at_1
      value: 16.0
    - type: map_at_3
      value: 22.967000000000002
    - type: map_at_5
      value: 26.177
    - type: map_at_10
      value: 28.427999999999997
    - type: map_at_20
      value: 29.229
    - type: map_at_100
      value: 29.725
    - type: map_at_1000
      value: 29.761
    - type: recall_at_1
      value: 16.0
    - type: recall_at_3
      value: 32.800000000000004
    - type: recall_at_5
      value: 47.0
    - type: recall_at_10
      value: 63.2
    - type: recall_at_20
      value: 74.6
    - type: recall_at_100
      value: 93.2
    - type: recall_at_1000
      value: 99.6
    - type: precision_at_1
      value: 16.0
    - type: precision_at_3
      value: 10.933
    - type: precision_at_5
      value: 9.4
    - type: precision_at_10
      value: 6.32
    - type: precision_at_20
      value: 3.73
    - type: precision_at_100
      value: 0.932
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 16.400000000000002
    - type: mrr_at_3
      value: 24.1333
    - type: mrr_at_5
      value: 26.043300000000002
    - type: mrr_at_10
      value: 28.3194
    - type: mrr_at_20
      value: 29.2356
    - type: mrr_at_100
      value: 29.7487
    - type: mrr_at_1000
      value: 29.786600000000004
    - type: nauc_ndcg_at_1_max
      value: 3.254
    - type: nauc_ndcg_at_1_std
      value: -14.7227
    - type: nauc_ndcg_at_1_diff1
      value: 37.6337
    - type: nauc_ndcg_at_3_max
      value: 7.615600000000001
    - type: nauc_ndcg_at_3_std
      value: -13.242799999999999
    - type: nauc_ndcg_at_3_diff1
      value: 22.9354
    - type: nauc_ndcg_at_5_max
      value: 11.186599999999999
    - type: nauc_ndcg_at_5_std
      value: -10.3925
    - type: nauc_ndcg_at_5_diff1
      value: 17.779600000000002
    - type: nauc_ndcg_at_10_max
      value: 9.4009
    - type: nauc_ndcg_at_10_std
      value: -10.864
    - type: nauc_ndcg_at_10_diff1
      value: 18.1759
    - type: nauc_ndcg_at_20_max
      value: 9.9435
    - type: nauc_ndcg_at_20_std
      value: -10.5532
    - type: nauc_ndcg_at_20_diff1
      value: 18.0746
    - type: nauc_ndcg_at_100_max
      value: 9.6817
    - type: nauc_ndcg_at_100_std
      value: -9.0056
    - type: nauc_ndcg_at_100_diff1
      value: 20.5883
    - type: nauc_ndcg_at_1000_max
      value: 9.1859
    - type: nauc_ndcg_at_1000_std
      value: -10.2839
    - type: nauc_ndcg_at_1000_diff1
      value: 21.3418
    - type: nauc_map_at_1_max
      value: 3.254
    - type: nauc_map_at_1_std
      value: -14.7227
    - type: nauc_map_at_1_diff1
      value: 37.6337
    - type: nauc_map_at_3_max
      value: 6.641800000000001
    - type: nauc_map_at_3_std
      value: -13.4988
    - type: nauc_map_at_3_diff1
      value: 26.174999999999997
    - type: nauc_map_at_5_max
      value: 8.6381
    - type: nauc_map_at_5_std
      value: -11.8414
    - type: nauc_map_at_5_diff1
      value: 23.1285
    - type: nauc_map_at_10_max
      value: 7.8475
    - type: nauc_map_at_10_std
      value: -12.021999999999998
    - type: nauc_map_at_10_diff1
      value: 23.3678
    - type: nauc_map_at_20_max
      value: 8.0317
    - type: nauc_map_at_20_std
      value: -11.8687
    - type: nauc_map_at_20_diff1
      value: 23.4456
    - type: nauc_map_at_100_max
      value: 7.9571000000000005
    - type: nauc_map_at_100_std
      value: -11.6699
    - type: nauc_map_at_100_diff1
      value: 23.7984
    - type: nauc_map_at_1000_max
      value: 7.943
    - type: nauc_map_at_1000_std
      value: -11.7087
    - type: nauc_map_at_1000_diff1
      value: 23.8186
    - type: nauc_recall_at_1_max
      value: 3.254
    - type: nauc_recall_at_1_std
      value: -14.7227
    - type: nauc_recall_at_1_diff1
      value: 37.6337
    - type: nauc_recall_at_3_max
      value: 9.9777
    - type: nauc_recall_at_3_std
      value: -12.645100000000001
    - type: nauc_recall_at_3_diff1
      value: 15.090600000000002
    - type: nauc_recall_at_5_max
      value: 17.8264
    - type: nauc_recall_at_5_std
      value: -6.5932
    - type: nauc_recall_at_5_diff1
      value: 4.3373
    - type: nauc_recall_at_10_max
      value: 13.5901
    - type: nauc_recall_at_10_std
      value: -7.5634999999999994
    - type: nauc_recall_at_10_diff1
      value: 3.2628999999999997
    - type: nauc_recall_at_20_max
      value: 16.8637
    - type: nauc_recall_at_20_std
      value: -5.876399999999999
    - type: nauc_recall_at_20_diff1
      value: -2.0105999999999997
    - type: nauc_recall_at_100_max
      value: 28.4163
    - type: nauc_recall_at_100_std
      value: 32.5479
    - type: nauc_recall_at_100_diff1
      value: 1.6202999999999999
    - type: nauc_recall_at_1000_max
      value: 86.1111
    - type: nauc_recall_at_1000_std
      value: 93.4641
    - type: nauc_recall_at_1000_diff1
      value: 63.8189
    - type: nauc_precision_at_1_max
      value: 3.254
    - type: nauc_precision_at_1_std
      value: -14.7227
    - type: nauc_precision_at_1_diff1
      value: 37.6337
    - type: nauc_precision_at_3_max
      value: 9.9777
    - type: nauc_precision_at_3_std
      value: -12.645100000000001
    - type: nauc_precision_at_3_diff1
      value: 15.090600000000002
    - type: nauc_precision_at_5_max
      value: 17.8264
    - type: nauc_precision_at_5_std
      value: -6.5932
    - type: nauc_precision_at_5_diff1
      value: 4.3373
    - type: nauc_precision_at_10_max
      value: 13.5901
    - type: nauc_precision_at_10_std
      value: -7.5634999999999994
    - type: nauc_precision_at_10_diff1
      value: 3.2628999999999997
    - type: nauc_precision_at_20_max
      value: 16.8637
    - type: nauc_precision_at_20_std
      value: -5.876399999999999
    - type: nauc_precision_at_20_diff1
      value: -2.0105999999999997
    - type: nauc_precision_at_100_max
      value: 28.4163
    - type: nauc_precision_at_100_std
      value: 32.5479
    - type: nauc_precision_at_100_diff1
      value: 1.6202999999999999
    - type: nauc_precision_at_1000_max
      value: 86.1111
    - type: nauc_precision_at_1000_std
      value: 93.4641
    - type: nauc_precision_at_1000_diff1
      value: 63.8189
    - type: nauc_mrr_at_1_max
      value: 7.7073
    - type: nauc_mrr_at_1_std
      value: -15.7727
    - type: nauc_mrr_at_1_diff1
      value: 36.2605
    - type: nauc_mrr_at_3_max
      value: 7.0968
    - type: nauc_mrr_at_3_std
      value: -13.9735
    - type: nauc_mrr_at_3_diff1
      value: 25.1765
    - type: nauc_mrr_at_5_max
      value: 7.2429
    - type: nauc_mrr_at_5_std
      value: -14.223099999999999
    - type: nauc_mrr_at_5_diff1
      value: 23.2141
    - type: nauc_mrr_at_10_max
      value: 8.1606
    - type: nauc_mrr_at_10_std
      value: -13.4187
    - type: nauc_mrr_at_10_diff1
      value: 22.9983
    - type: nauc_mrr_at_20_max
      value: 8.39
    - type: nauc_mrr_at_20_std
      value: -13.28
    - type: nauc_mrr_at_20_diff1
      value: 22.830000000000002
    - type: nauc_mrr_at_100_max
      value: 8.3666
    - type: nauc_mrr_at_100_std
      value: -13.112599999999999
    - type: nauc_mrr_at_100_diff1
      value: 23.1988
    - type: nauc_mrr_at_1000_max
      value: 8.3461
    - type: nauc_mrr_at_1000_std
      value: -13.159799999999999
    - type: nauc_mrr_at_1000_diff1
      value: 23.217499999999998
    - type: main_score
      value: 36.619
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB DBPedia (default)
      revision: c0f706b76e590d620bd6618b3ca8efdd34e2d659
      split: test
      type: mteb/dbpedia
    metrics:
    - type: ndcg_at_1
      value: 54.37499999999999
    - type: ndcg_at_3
      value: 44.463
    - type: ndcg_at_5
      value: 41.276
    - type: ndcg_at_10
      value: 39.409
    - type: ndcg_at_20
      value: 38.884
    - type: ndcg_at_100
      value: 44.382
    - type: ndcg_at_1000
      value: 52.48500000000001
    - type: map_at_1
      value: 8.709999999999999
    - type: map_at_3
      value: 13.974
    - type: map_at_5
      value: 16.104
    - type: map_at_10
      value: 19.218
    - type: map_at_20
      value: 21.966
    - type: map_at_100
      value: 26.290999999999997
    - type: map_at_1000
      value: 27.985
    - type: recall_at_1
      value: 8.709999999999999
    - type: recall_at_3
      value: 15.516
    - type: recall_at_5
      value: 18.907
    - type: recall_at_10
      value: 25.27
    - type: recall_at_20
      value: 31.968000000000004
    - type: recall_at_100
      value: 51.849999999999994
    - type: recall_at_1000
      value: 76.491
    - type: precision_at_1
      value: 67.25
    - type: precision_at_3
      value: 48.167
    - type: precision_at_5
      value: 39.4
    - type: precision_at_10
      value: 30.55
    - type: precision_at_20
      value: 22.75
    - type: precision_at_100
      value: 9.588000000000001
    - type: precision_at_1000
      value: 2.118
    - type: mrr_at_1
      value: 67.25
    - type: mrr_at_3
      value: 73.83330000000001
    - type: mrr_at_5
      value: 74.3083
    - type: mrr_at_10
      value: 75.03699999999999
    - type: mrr_at_20
      value: 75.1468
    - type: mrr_at_100
      value: 75.3182
    - type: mrr_at_1000
      value: 75.3253
    - type: nauc_ndcg_at_1_max
      value: 30.7815
    - type: nauc_ndcg_at_1_std
      value: 18.9823
    - type: nauc_ndcg_at_1_diff1
      value: 38.7185
    - type: nauc_ndcg_at_3_max
      value: 27.3482
    - type: nauc_ndcg_at_3_std
      value: 20.1357
    - type: nauc_ndcg_at_3_diff1
      value: 24.9478
    - type: nauc_ndcg_at_5_max
      value: 23.8231
    - type: nauc_ndcg_at_5_std
      value: 19.8595
    - type: nauc_ndcg_at_5_diff1
      value: 20.5147
    - type: nauc_ndcg_at_10_max
      value: 19.8984
    - type: nauc_ndcg_at_10_std
      value: 16.6632
    - type: nauc_ndcg_at_10_diff1
      value: 18.5195
    - type: nauc_ndcg_at_20_max
      value: 15.437000000000001
    - type: nauc_ndcg_at_20_std
      value: 13.8071
    - type: nauc_ndcg_at_20_diff1
      value: 18.0289
    - type: nauc_ndcg_at_100_max
      value: 15.042900000000001
    - type: nauc_ndcg_at_100_std
      value: 18.1034
    - type: nauc_ndcg_at_100_diff1
      value: 16.5884
    - type: nauc_ndcg_at_1000_max
      value: 24.6937
    - type: nauc_ndcg_at_1000_std
      value: 28.625
    - type: nauc_ndcg_at_1000_diff1
      value: 16.9271
    - type: nauc_map_at_1_max
      value: -7.1981
    - type: nauc_map_at_1_std
      value: -20.8768
    - type: nauc_map_at_1_diff1
      value: 24.6797
    - type: nauc_map_at_3_max
      value: -4.8358
    - type: nauc_map_at_3_std
      value: -16.6611
    - type: nauc_map_at_3_diff1
      value: 18.9037
    - type: nauc_map_at_5_max
      value: -3.4354999999999998
    - type: nauc_map_at_5_std
      value: -14.018600000000001
    - type: nauc_map_at_5_diff1
      value: 17.516499999999997
    - type: nauc_map_at_10_max
      value: -0.9939999999999999
    - type: nauc_map_at_10_std
      value: -8.484
    - type: nauc_map_at_10_diff1
      value: 15.8007
    - type: nauc_map_at_20_max
      value: 3.2260999999999997
    - type: nauc_map_at_20_std
      value: -0.8369
    - type: nauc_map_at_20_diff1
      value: 15.8524
    - type: nauc_map_at_100_max
      value: 9.8084
    - type: nauc_map_at_100_std
      value: 11.7005
    - type: nauc_map_at_100_diff1
      value: 16.5458
    - type: nauc_map_at_1000_max
      value: 12.7583
    - type: nauc_map_at_1000_std
      value: 15.331
    - type: nauc_map_at_1000_diff1
      value: 16.7243
    - type: nauc_recall_at_1_max
      value: -7.1981
    - type: nauc_recall_at_1_std
      value: -20.8768
    - type: nauc_recall_at_1_diff1
      value: 24.6797
    - type: nauc_recall_at_3_max
      value: -8.7416
    - type: nauc_recall_at_3_std
      value: -18.1497
    - type: nauc_recall_at_3_diff1
      value: 13.2151
    - type: nauc_recall_at_5_max
      value: -7.7954
    - type: nauc_recall_at_5_std
      value: -16.4247
    - type: nauc_recall_at_5_diff1
      value: 11.3209
    - type: nauc_recall_at_10_max
      value: -6.8051
    - type: nauc_recall_at_10_std
      value: -11.8753
    - type: nauc_recall_at_10_diff1
      value: 9.1489
    - type: nauc_recall_at_20_max
      value: -3.7832999999999997
    - type: nauc_recall_at_20_std
      value: -4.0681
    - type: nauc_recall_at_20_diff1
      value: 7.769299999999999
    - type: nauc_recall_at_100_max
      value: 2.4143000000000003
    - type: nauc_recall_at_100_std
      value: 13.5572
    - type: nauc_recall_at_100_diff1
      value: 6.3968
    - type: nauc_recall_at_1000_max
      value: 14.8639
    - type: nauc_recall_at_1000_std
      value: 34.389900000000004
    - type: nauc_recall_at_1000_diff1
      value: 2.3819
    - type: nauc_precision_at_1_max
      value: 39.8074
    - type: nauc_precision_at_1_std
      value: 29.7269
    - type: nauc_precision_at_1_diff1
      value: 46.7701
    - type: nauc_precision_at_3_max
      value: 32.2757
    - type: nauc_precision_at_3_std
      value: 30.7486
    - type: nauc_precision_at_3_diff1
      value: 13.880400000000002
    - type: nauc_precision_at_5_max
      value: 31.016
    - type: nauc_precision_at_5_std
      value: 37.9799
    - type: nauc_precision_at_5_diff1
      value: 7.4082
    - type: nauc_precision_at_10_max
      value: 32.268
    - type: nauc_precision_at_10_std
      value: 43.9588
    - type: nauc_precision_at_10_diff1
      value: 4.3159
    - type: nauc_precision_at_20_max
      value: 32.264199999999995
    - type: nauc_precision_at_20_std
      value: 48.2933
    - type: nauc_precision_at_20_diff1
      value: 3.8432
    - type: nauc_precision_at_100_max
      value: 30.725799999999996
    - type: nauc_precision_at_100_std
      value: 49.6683
    - type: nauc_precision_at_100_diff1
      value: 0.0351
    - type: nauc_precision_at_1000_max
      value: 28.237299999999998
    - type: nauc_precision_at_1000_std
      value: 24.8433
    - type: nauc_precision_at_1000_diff1
      value: 3.6408000000000005
    - type: nauc_mrr_at_1_max
      value: 39.8074
    - type: nauc_mrr_at_1_std
      value: 29.7269
    - type: nauc_mrr_at_1_diff1
      value: 46.7701
    - type: nauc_mrr_at_3_max
      value: 42.7825
    - type: nauc_mrr_at_3_std
      value: 32.467800000000004
    - type: nauc_mrr_at_3_diff1
      value: 43.7056
    - type: nauc_mrr_at_5_max
      value: 43.0631
    - type: nauc_mrr_at_5_std
      value: 32.859
    - type: nauc_mrr_at_5_diff1
      value: 43.646
    - type: nauc_mrr_at_10_max
      value: 42.8307
    - type: nauc_mrr_at_10_std
      value: 32.8042
    - type: nauc_mrr_at_10_diff1
      value: 43.3566
    - type: nauc_mrr_at_20_max
      value: 42.9185
    - type: nauc_mrr_at_20_std
      value: 32.723600000000005
    - type: nauc_mrr_at_20_diff1
      value: 43.6419
    - type: nauc_mrr_at_100_max
      value: 43.006699999999995
    - type: nauc_mrr_at_100_std
      value: 32.628800000000005
    - type: nauc_mrr_at_100_diff1
      value: 43.935
    - type: nauc_mrr_at_1000_max
      value: 42.9879
    - type: nauc_mrr_at_1000_std
      value: 32.6121
    - type: nauc_mrr_at_1000_diff1
      value: 43.9284
    - type: main_score
      value: 39.409
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB EmotionClassification (default)
      revision: 4f58c6b202a23cf9a4da393831edf4f9183cad37
      split: test
      type: mteb/emotion
    metrics:
    - type: accuracy
      value: 40.949999999999996
    - type: f1
      value: 37.1674
    - type: f1_weighted
      value: 43.1842
    - type: main_score
      value: 40.949999999999996
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB FEVER (default)
      revision: bea83ef9e8fb933d90a2f1d5515737465d613e12
      split: test
      type: mteb/fever
    metrics:
    - type: ndcg_at_1
      value: 85.179
    - type: ndcg_at_3
      value: 87.304
    - type: ndcg_at_5
      value: 87.862
    - type: ndcg_at_10
      value: 88.229
    - type: ndcg_at_20
      value: 88.49000000000001
    - type: ndcg_at_100
      value: 88.84
    - type: ndcg_at_1000
      value: 89.116
    - type: map_at_1
      value: 78.993
    - type: map_at_3
      value: 84.37
    - type: map_at_5
      value: 84.812
    - type: map_at_10
      value: 85.02
    - type: map_at_20
      value: 85.114
    - type: map_at_100
      value: 85.18599999999999
    - type: map_at_1000
      value: 85.2
    - type: recall_at_1
      value: 78.993
    - type: recall_at_3
      value: 89.96499999999999
    - type: recall_at_5
      value: 91.562
    - type: recall_at_10
      value: 92.685
    - type: recall_at_20
      value: 93.595
    - type: recall_at_100
      value: 95.16
    - type: recall_at_1000
      value: 96.943
    - type: precision_at_1
      value: 85.179
    - type: precision_at_3
      value: 32.543
    - type: precision_at_5
      value: 19.930999999999997
    - type: precision_at_10
      value: 10.129000000000001
    - type: precision_at_20
      value: 5.140000000000001
    - type: precision_at_100
      value: 1.06
    - type: precision_at_1000
      value: 0.11
    - type: mrr_at_1
      value: 85.1785
    - type: mrr_at_3
      value: 90.3215
    - type: mrr_at_5
      value: 90.6223
    - type: mrr_at_10
      value: 90.74449999999999
    - type: mrr_at_20
      value: 90.78389999999999
    - type: mrr_at_100
      value: 90.79899999999999
    - type: mrr_at_1000
      value: 90.80080000000001
    - type: nauc_ndcg_at_1_max
      value: 42.509
    - type: nauc_ndcg_at_1_std
      value: -14.4135
    - type: nauc_ndcg_at_1_diff1
      value: 69.351
    - type: nauc_ndcg_at_3_max
      value: 31.848599999999998
    - type: nauc_ndcg_at_3_std
      value: -8.8348
    - type: nauc_ndcg_at_3_diff1
      value: 43.6934
    - type: nauc_ndcg_at_5_max
      value: 30.5029
    - type: nauc_ndcg_at_5_std
      value: -7.1606000000000005
    - type: nauc_ndcg_at_5_diff1
      value: 43.1125
    - type: nauc_ndcg_at_10_max
      value: 30.383900000000004
    - type: nauc_ndcg_at_10_std
      value: -6.112299999999999
    - type: nauc_ndcg_at_10_diff1
      value: 42.9948
    - type: nauc_ndcg_at_20_max
      value: 30.6167
    - type: nauc_ndcg_at_20_std
      value: -5.6432
    - type: nauc_ndcg_at_20_diff1
      value: 43.247600000000006
    - type: nauc_ndcg_at_100_max
      value: 31.2245
    - type: nauc_ndcg_at_100_std
      value: -5.3287
    - type: nauc_ndcg_at_100_diff1
      value: 43.5092
    - type: nauc_ndcg_at_1000_max
      value: 31.724999999999998
    - type: nauc_ndcg_at_1000_std
      value: -5.5252
    - type: nauc_ndcg_at_1000_diff1
      value: 44.1117
    - type: nauc_map_at_1_max
      value: 33.535900000000005
    - type: nauc_map_at_1_std
      value: -7.5043
    - type: nauc_map_at_1_diff1
      value: 51.1658
    - type: nauc_map_at_3_max
      value: 30.357499999999998
    - type: nauc_map_at_3_std
      value: -7.0673
    - type: nauc_map_at_3_diff1
      value: 43.169000000000004
    - type: nauc_map_at_5_max
      value: 30.1609
    - type: nauc_map_at_5_std
      value: -6.2828
    - type: nauc_map_at_5_diff1
      value: 43.22
    - type: nauc_map_at_10_max
      value: 30.2687
    - type: nauc_map_at_10_std
      value: -5.931299999999999
    - type: nauc_map_at_10_diff1
      value: 43.3113
    - type: nauc_map_at_20_max
      value: 30.3425
    - type: nauc_map_at_20_std
      value: -5.827999999999999
    - type: nauc_map_at_20_diff1
      value: 43.378
    - type: nauc_map_at_100_max
      value: 30.4597
    - type: nauc_map_at_100_std
      value: -5.781
    - type: nauc_map_at_100_diff1
      value: 43.4338
    - type: nauc_map_at_1000_max
      value: 30.4815
    - type: nauc_map_at_1000_std
      value: -5.7874
    - type: nauc_map_at_1000_diff1
      value: 43.4604
    - type: nauc_recall_at_1_max
      value: 33.535900000000005
    - type: nauc_recall_at_1_std
      value: -7.5043
    - type: nauc_recall_at_1_diff1
      value: 51.1658
    - type: nauc_recall_at_3_max
      value: 21.5412
    - type: nauc_recall_at_3_std
      value: -5.3411
    - type: nauc_recall_at_3_diff1
      value: 22.9753
    - type: nauc_recall_at_5_max
      value: 18.2607
    - type: nauc_recall_at_5_std
      value: 0.4319
    - type: nauc_recall_at_5_diff1
      value: 18.4494
    - type: nauc_recall_at_10_max
      value: 16.9918
    - type: nauc_recall_at_10_std
      value: 5.6791
    - type: nauc_recall_at_10_diff1
      value: 14.8096
    - type: nauc_recall_at_20_max
      value: 16.2394
    - type: nauc_recall_at_20_std
      value: 10.014000000000001
    - type: nauc_recall_at_20_diff1
      value: 12.6674
    - type: nauc_recall_at_100_max
      value: 17.160700000000002
    - type: nauc_recall_at_100_std
      value: 17.7282
    - type: nauc_recall_at_100_diff1
      value: 6.4750000000000005
    - type: nauc_recall_at_1000_max
      value: 18.7047
    - type: nauc_recall_at_1000_std
      value: 26.4285
    - type: nauc_recall_at_1000_diff1
      value: -0.4528
    - type: nauc_precision_at_1_max
      value: 42.509
    - type: nauc_precision_at_1_std
      value: -14.4135
    - type: nauc_precision_at_1_diff1
      value: 69.351
    - type: nauc_precision_at_3_max
      value: 21.5337
    - type: nauc_precision_at_3_std
      value: -18.1489
    - type: nauc_precision_at_3_diff1
      value: 23.7103
    - type: nauc_precision_at_5_max
      value: 10.8839
    - type: nauc_precision_at_5_std
      value: -8.7334
    - type: nauc_precision_at_5_diff1
      value: 12.0412
    - type: nauc_precision_at_10_max
      value: 5.632000000000001
    - type: nauc_precision_at_10_std
      value: -1.2274
    - type: nauc_precision_at_10_diff1
      value: 3.2148000000000003
    - type: nauc_precision_at_20_max
      value: 3.6290999999999998
    - type: nauc_precision_at_20_std
      value: 3.1643
    - type: nauc_precision_at_20_diff1
      value: -2.106
    - type: nauc_precision_at_100_max
      value: 3.749
    - type: nauc_precision_at_100_std
      value: 5.944599999999999
    - type: nauc_precision_at_100_diff1
      value: -8.2121
    - type: nauc_precision_at_1000_max
      value: 3.9972
    - type: nauc_precision_at_1000_std
      value: 3.2577000000000003
    - type: nauc_precision_at_1000_diff1
      value: -8.6116
    - type: nauc_mrr_at_1_max
      value: 42.509
    - type: nauc_mrr_at_1_std
      value: -14.4135
    - type: nauc_mrr_at_1_diff1
      value: 69.351
    - type: nauc_mrr_at_3_max
      value: 41.805
    - type: nauc_mrr_at_3_std
      value: -17.8756
    - type: nauc_mrr_at_3_diff1
      value: 65.21050000000001
    - type: nauc_mrr_at_5_max
      value: 41.9114
    - type: nauc_mrr_at_5_std
      value: -17.1294
    - type: nauc_mrr_at_5_diff1
      value: 65.5444
    - type: nauc_mrr_at_10_max
      value: 42.1507
    - type: nauc_mrr_at_10_std
      value: -16.7196
    - type: nauc_mrr_at_10_diff1
      value: 65.76480000000001
    - type: nauc_mrr_at_20_max
      value: 42.1918
    - type: nauc_mrr_at_20_std
      value: -16.6012
    - type: nauc_mrr_at_20_diff1
      value: 65.9105
    - type: nauc_mrr_at_100_max
      value: 42.1853
    - type: nauc_mrr_at_100_std
      value: -16.578799999999998
    - type: nauc_mrr_at_100_diff1
      value: 65.9277
    - type: nauc_mrr_at_1000_max
      value: 42.1787
    - type: nauc_mrr_at_1000_std
      value: -16.5811
    - type: nauc_mrr_at_1000_diff1
      value: 65.9297
    - type: main_score
      value: 88.229
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB FiQA2018 (default)
      revision: 27a168819829fe9bcd655c2df245fb19452e8e06
      split: test
      type: mteb/fiqa
    metrics:
    - type: ndcg_at_1
      value: 44.599
    - type: ndcg_at_3
      value: 41.597
    - type: ndcg_at_5
      value: 42.611
    - type: ndcg_at_10
      value: 44.931
    - type: ndcg_at_20
      value: 47.727000000000004
    - type: ndcg_at_100
      value: 51.914
    - type: ndcg_at_1000
      value: 54.674
    - type: map_at_1
      value: 22.586000000000002
    - type: map_at_3
      value: 32.445
    - type: map_at_5
      value: 34.951
    - type: map_at_10
      value: 36.836
    - type: map_at_20
      value: 37.958
    - type: map_at_100
      value: 38.863
    - type: map_at_1000
      value: 39.041
    - type: recall_at_1
      value: 22.586000000000002
    - type: recall_at_3
      value: 37.802
    - type: recall_at_5
      value: 43.86
    - type: recall_at_10
      value: 51.519999999999996
    - type: recall_at_20
      value: 60.22
    - type: recall_at_100
      value: 77.251
    - type: recall_at_1000
      value: 93.503
    - type: precision_at_1
      value: 44.599
    - type: precision_at_3
      value: 27.622999999999998
    - type: precision_at_5
      value: 20.093
    - type: precision_at_10
      value: 12.346
    - type: precision_at_20
      value: 7.353
    - type: precision_at_100
      value: 1.951
    - type: precision_at_1000
      value: 0.244
    - type: mrr_at_1
      value: 44.5988
    - type: mrr_at_3
      value: 51.157399999999996
    - type: mrr_at_5
      value: 52.4228
    - type: mrr_at_10
      value: 53.4708
    - type: mrr_at_20
      value: 53.898500000000006
    - type: mrr_at_100
      value: 54.18619999999999
    - type: mrr_at_1000
      value: 54.2227
    - type: nauc_ndcg_at_1_max
      value: 41.8311
    - type: nauc_ndcg_at_1_std
      value: -1.4024999999999999
    - type: nauc_ndcg_at_1_diff1
      value: 51.9037
    - type: nauc_ndcg_at_3_max
      value: 35.448299999999996
    - type: nauc_ndcg_at_3_std
      value: -0.3253
    - type: nauc_ndcg_at_3_diff1
      value: 40.5332
    - type: nauc_ndcg_at_5_max
      value: 34.3939
    - type: nauc_ndcg_at_5_std
      value: 0.5177
    - type: nauc_ndcg_at_5_diff1
      value: 39.729
    - type: nauc_ndcg_at_10_max
      value: 32.8185
    - type: nauc_ndcg_at_10_std
      value: 1.2571
    - type: nauc_ndcg_at_10_diff1
      value: 39.358
    - type: nauc_ndcg_at_20_max
      value: 34.4751
    - type: nauc_ndcg_at_20_std
      value: 3.0460000000000003
    - type: nauc_ndcg_at_20_diff1
      value: 40.474700000000006
    - type: nauc_ndcg_at_100_max
      value: 37.079699999999995
    - type: nauc_ndcg_at_100_std
      value: 6.704400000000001
    - type: nauc_ndcg_at_100_diff1
      value: 41.145199999999996
    - type: nauc_ndcg_at_1000_max
      value: 37.5561
    - type: nauc_ndcg_at_1000_std
      value: 5.4764
    - type: nauc_ndcg_at_1000_diff1
      value: 41.104400000000005
    - type: nauc_map_at_1_max
      value: 22.570899999999998
    - type: nauc_map_at_1_std
      value: -4.3153
    - type: nauc_map_at_1_diff1
      value: 45.949400000000004
    - type: nauc_map_at_3_max
      value: 27.0957
    - type: nauc_map_at_3_std
      value: -2.0714
    - type: nauc_map_at_3_diff1
      value: 40.2278
    - type: nauc_map_at_5_max
      value: 29.744500000000002
    - type: nauc_map_at_5_std
      value: -0.6752
    - type: nauc_map_at_5_diff1
      value: 39.44
    - type: nauc_map_at_10_max
      value: 30.2678
    - type: nauc_map_at_10_std
      value: -0.0069
    - type: nauc_map_at_10_diff1
      value: 38.9648
    - type: nauc_map_at_20_max
      value: 31.381700000000002
    - type: nauc_map_at_20_std
      value: 0.765
    - type: nauc_map_at_20_diff1
      value: 39.3088
    - type: nauc_map_at_100_max
      value: 32.1076
    - type: nauc_map_at_100_std
      value: 1.4984000000000002
    - type: nauc_map_at_100_diff1
      value: 39.4675
    - type: nauc_map_at_1000_max
      value: 32.1799
    - type: nauc_map_at_1000_std
      value: 1.4738
    - type: nauc_map_at_1000_diff1
      value: 39.4786
    - type: nauc_recall_at_1_max
      value: 22.570899999999998
    - type: nauc_recall_at_1_std
      value: -4.3153
    - type: nauc_recall_at_1_diff1
      value: 45.949400000000004
    - type: nauc_recall_at_3_max
      value: 22.0782
    - type: nauc_recall_at_3_std
      value: -1.7135999999999998
    - type: nauc_recall_at_3_diff1
      value: 33.5696
    - type: nauc_recall_at_5_max
      value: 24.9421
    - type: nauc_recall_at_5_std
      value: 0.47019999999999995
    - type: nauc_recall_at_5_diff1
      value: 31.660899999999998
    - type: nauc_recall_at_10_max
      value: 22.847
    - type: nauc_recall_at_10_std
      value: 2.1398
    - type: nauc_recall_at_10_diff1
      value: 27.879199999999997
    - type: nauc_recall_at_20_max
      value: 24.476
    - type: nauc_recall_at_20_std
      value: 7.3819
    - type: nauc_recall_at_20_diff1
      value: 29.717100000000002
    - type: nauc_recall_at_100_max
      value: 33.1008
    - type: nauc_recall_at_100_std
      value: 32.008900000000004
    - type: nauc_recall_at_100_diff1
      value: 29.1164
    - type: nauc_recall_at_1000_max
      value: 39.5742
    - type: nauc_recall_at_1000_std
      value: 51.944199999999995
    - type: nauc_recall_at_1000_diff1
      value: 17.8932
    - type: nauc_precision_at_1_max
      value: 41.8311
    - type: nauc_precision_at_1_std
      value: -1.4024999999999999
    - type: nauc_precision_at_1_diff1
      value: 51.9037
    - type: nauc_precision_at_3_max
      value: 38.707300000000004
    - type: nauc_precision_at_3_std
      value: 3.3242000000000003
    - type: nauc_precision_at_3_diff1
      value: 26.32
    - type: nauc_precision_at_5_max
      value: 40.4051
    - type: nauc_precision_at_5_std
      value: 7.2255
    - type: nauc_precision_at_5_diff1
      value: 20.524
    - type: nauc_precision_at_10_max
      value: 37.024
    - type: nauc_precision_at_10_std
      value: 8.871
    - type: nauc_precision_at_10_diff1
      value: 14.985100000000001
    - type: nauc_precision_at_20_max
      value: 39.8142
    - type: nauc_precision_at_20_std
      value: 12.9133
    - type: nauc_precision_at_20_diff1
      value: 13.5855
    - type: nauc_precision_at_100_max
      value: 36.8128
    - type: nauc_precision_at_100_std
      value: 17.273
    - type: nauc_precision_at_100_diff1
      value: 7.706799999999999
    - type: nauc_precision_at_1000_max
      value: 29.197699999999998
    - type: nauc_precision_at_1000_std
      value: 10.452200000000001
    - type: nauc_precision_at_1000_diff1
      value: -0.43429999999999996
    - type: nauc_mrr_at_1_max
      value: 41.8311
    - type: nauc_mrr_at_1_std
      value: -1.4024999999999999
    - type: nauc_mrr_at_1_diff1
      value: 51.9037
    - type: nauc_mrr_at_3_max
      value: 41.5348
    - type: nauc_mrr_at_3_std
      value: 0.47200000000000003
    - type: nauc_mrr_at_3_diff1
      value: 48.2132
    - type: nauc_mrr_at_5_max
      value: 41.4712
    - type: nauc_mrr_at_5_std
      value: 0.9362
    - type: nauc_mrr_at_5_diff1
      value: 47.7862
    - type: nauc_mrr_at_10_max
      value: 41.3833
    - type: nauc_mrr_at_10_std
      value: 0.9305000000000001
    - type: nauc_mrr_at_10_diff1
      value: 47.8177
    - type: nauc_mrr_at_20_max
      value: 41.5143
    - type: nauc_mrr_at_20_std
      value: 1.2017
    - type: nauc_mrr_at_20_diff1
      value: 48.0106
    - type: nauc_mrr_at_100_max
      value: 41.6027
    - type: nauc_mrr_at_100_std
      value: 1.3906999999999998
    - type: nauc_mrr_at_100_diff1
      value: 48.0719
    - type: nauc_mrr_at_1000_max
      value: 41.597
    - type: nauc_mrr_at_1000_std
      value: 1.3443
    - type: nauc_mrr_at_1000_diff1
      value: 48.0767
    - type: main_score
      value: 44.931
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB HotpotQA (default)
      revision: ab518f4d6fcca38d87c25209f94beba119d02014
      split: test
      type: mteb/hotpotqa
    metrics:
    - type: ndcg_at_1
      value: 76.354
    - type: ndcg_at_3
      value: 62.900999999999996
    - type: ndcg_at_5
      value: 65.68
    - type: ndcg_at_10
      value: 67.776
    - type: ndcg_at_20
      value: 69.144
    - type: ndcg_at_100
      value: 70.85000000000001
    - type: ndcg_at_1000
      value: 72.151
    - type: map_at_1
      value: 38.177
    - type: map_at_3
      value: 55.554
    - type: map_at_5
      value: 57.774
    - type: map_at_10
      value: 59.022
    - type: map_at_20
      value: 59.574000000000005
    - type: map_at_100
      value: 59.925
    - type: map_at_1000
      value: 59.99
    - type: recall_at_1
      value: 38.177
    - type: recall_at_3
      value: 60.169
    - type: recall_at_5
      value: 65.63799999999999
    - type: recall_at_10
      value: 70.878
    - type: recall_at_20
      value: 75.267
    - type: recall_at_100
      value: 82.822
    - type: recall_at_1000
      value: 91.472
    - type: precision_at_1
      value: 76.354
    - type: precision_at_3
      value: 40.113
    - type: precision_at_5
      value: 26.255
    - type: precision_at_10
      value: 14.176
    - type: precision_at_20
      value: 7.527
    - type: precision_at_100
      value: 1.656
    - type: precision_at_1000
      value: 0.183
    - type: mrr_at_1
      value: 76.3538
    - type: mrr_at_3
      value: 81.7218
    - type: mrr_at_5
      value: 82.3403
    - type: mrr_at_10
      value: 82.7021
    - type: mrr_at_20
      value: 82.8339
    - type: mrr_at_100
      value: 82.88889999999999
    - type: mrr_at_1000
      value: 82.8978
    - type: nauc_ndcg_at_1_max
      value: 45.4675
    - type: nauc_ndcg_at_1_std
      value: -8.5846
    - type: nauc_ndcg_at_1_diff1
      value: 67.2619
    - type: nauc_ndcg_at_3_max
      value: 29.083399999999997
    - type: nauc_ndcg_at_3_std
      value: 0.9821
    - type: nauc_ndcg_at_3_diff1
      value: 22.708000000000002
    - type: nauc_ndcg_at_5_max
      value: 29.0541
    - type: nauc_ndcg_at_5_std
      value: 3.5778999999999996
    - type: nauc_ndcg_at_5_diff1
      value: 20.8512
    - type: nauc_ndcg_at_10_max
      value: 28.6135
    - type: nauc_ndcg_at_10_std
      value: 5.3694
    - type: nauc_ndcg_at_10_diff1
      value: 19.913700000000002
    - type: nauc_ndcg_at_20_max
      value: 28.971000000000004
    - type: nauc_ndcg_at_20_std
      value: 6.6706
    - type: nauc_ndcg_at_20_diff1
      value: 20.015900000000002
    - type: nauc_ndcg_at_100_max
      value: 29.2235
    - type: nauc_ndcg_at_100_std
      value: 7.5165
    - type: nauc_ndcg_at_100_diff1
      value: 20.703
    - type: nauc_ndcg_at_1000_max
      value: 29.808
    - type: nauc_ndcg_at_1000_std
      value: 7.0276000000000005
    - type: nauc_ndcg_at_1000_diff1
      value: 21.8394
    - type: nauc_map_at_1_max
      value: 45.4675
    - type: nauc_map_at_1_std
      value: -8.5846
    - type: nauc_map_at_1_diff1
      value: 67.2619
    - type: nauc_map_at_3_max
      value: 25.374200000000002
    - type: nauc_map_at_3_std
      value: 1.4205
    - type: nauc_map_at_3_diff1
      value: 16.7465
    - type: nauc_map_at_5_max
      value: 25.5649
    - type: nauc_map_at_5_std
      value: 3.2438000000000002
    - type: nauc_map_at_5_diff1
      value: 15.676200000000001
    - type: nauc_map_at_10_max
      value: 25.4328
    - type: nauc_map_at_10_std
      value: 4.198799999999999
    - type: nauc_map_at_10_diff1
      value: 15.3134
    - type: nauc_map_at_20_max
      value: 25.583299999999998
    - type: nauc_map_at_20_std
      value: 4.6277
    - type: nauc_map_at_20_diff1
      value: 15.4013
    - type: nauc_map_at_100_max
      value: 25.647100000000002
    - type: nauc_map_at_100_std
      value: 4.7775
    - type: nauc_map_at_100_diff1
      value: 15.543999999999999
    - type: nauc_map_at_1000_max
      value: 25.672299999999996
    - type: nauc_map_at_1000_std
      value: 4.7689
    - type: nauc_map_at_1000_diff1
      value: 15.5824
    - type: nauc_recall_at_1_max
      value: 45.4675
    - type: nauc_recall_at_1_std
      value: -8.5846
    - type: nauc_recall_at_1_diff1
      value: 67.2619
    - type: nauc_recall_at_3_max
      value: 23.5896
    - type: nauc_recall_at_3_std
      value: 4.3086
    - type: nauc_recall_at_3_diff1
      value: 8.8109
    - type: nauc_recall_at_5_max
      value: 22.2473
    - type: nauc_recall_at_5_std
      value: 9.2394
    - type: nauc_recall_at_5_diff1
      value: 4.0969
    - type: nauc_recall_at_10_max
      value: 19.930600000000002
    - type: nauc_recall_at_10_std
      value: 14.0805
    - type: nauc_recall_at_10_diff1
      value: -0.1729
    - type: nauc_recall_at_20_max
      value: 19.938
    - type: nauc_recall_at_20_std
      value: 19.3764
    - type: nauc_recall_at_20_diff1
      value: -2.1292999999999997
    - type: nauc_recall_at_100_max
      value: 18.3819
    - type: nauc_recall_at_100_std
      value: 27.5254
    - type: nauc_recall_at_100_diff1
      value: -4.7437
    - type: nauc_recall_at_1000_max
      value: 20.441699999999997
    - type: nauc_recall_at_1000_std
      value: 35.8119
    - type: nauc_recall_at_1000_diff1
      value: -6.1713
    - type: nauc_precision_at_1_max
      value: 45.4675
    - type: nauc_precision_at_1_std
      value: -8.5846
    - type: nauc_precision_at_1_diff1
      value: 67.2619
    - type: nauc_precision_at_3_max
      value: 23.5896
    - type: nauc_precision_at_3_std
      value: 4.3086
    - type: nauc_precision_at_3_diff1
      value: 8.8109
    - type: nauc_precision_at_5_max
      value: 22.2473
    - type: nauc_precision_at_5_std
      value: 9.2394
    - type: nauc_precision_at_5_diff1
      value: 4.0969
    - type: nauc_precision_at_10_max
      value: 19.930600000000002
    - type: nauc_precision_at_10_std
      value: 14.0805
    - type: nauc_precision_at_10_diff1
      value: -0.1729
    - type: nauc_precision_at_20_max
      value: 19.938
    - type: nauc_precision_at_20_std
      value: 19.3764
    - type: nauc_precision_at_20_diff1
      value: -2.1292999999999997
    - type: nauc_precision_at_100_max
      value: 18.3819
    - type: nauc_precision_at_100_std
      value: 27.5254
    - type: nauc_precision_at_100_diff1
      value: -4.7437
    - type: nauc_precision_at_1000_max
      value: 20.441699999999997
    - type: nauc_precision_at_1000_std
      value: 35.8119
    - type: nauc_precision_at_1000_diff1
      value: -6.1713
    - type: nauc_mrr_at_1_max
      value: 45.4675
    - type: nauc_mrr_at_1_std
      value: -8.5846
    - type: nauc_mrr_at_1_diff1
      value: 67.2619
    - type: nauc_mrr_at_3_max
      value: 49.182700000000004
    - type: nauc_mrr_at_3_std
      value: -6.6154
    - type: nauc_mrr_at_3_diff1
      value: 65.8318
    - type: nauc_mrr_at_5_max
      value: 49.1926
    - type: nauc_mrr_at_5_std
      value: -6.059699999999999
    - type: nauc_mrr_at_5_diff1
      value: 65.819
    - type: nauc_mrr_at_10_max
      value: 49.0188
    - type: nauc_mrr_at_10_std
      value: -5.976
    - type: nauc_mrr_at_10_diff1
      value: 65.962
    - type: nauc_mrr_at_20_max
      value: 49.0418
    - type: nauc_mrr_at_20_std
      value: -5.9215
    - type: nauc_mrr_at_20_diff1
      value: 66.0577
    - type: nauc_mrr_at_100_max
      value: 48.9901
    - type: nauc_mrr_at_100_std
      value: -5.9538
    - type: nauc_mrr_at_100_diff1
      value: 66.0463
    - type: nauc_mrr_at_1000_max
      value: 48.9822
    - type: nauc_mrr_at_1000_std
      value: -5.9649
    - type: nauc_mrr_at_1000_diff1
      value: 66.0457
    - type: main_score
      value: 67.776
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB ImdbClassification (default)
      revision: 3d86128a09e091d6018b6d26cad27f2739fc2db7
      split: test
      type: mteb/imdb
    metrics:
    - type: accuracy
      value: 64.4052
    - type: f1
      value: 64.2124
    - type: f1_weighted
      value: 64.2124
    - type: ap
      value: 59.430899999999994
    - type: ap_weighted
      value: 59.430899999999994
    - type: main_score
      value: 64.4052
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB MSMARCO (default)
      revision: c5a29a104738b98a9e76336939199e264163d4a0
      split: dev
      type: mteb/msmarco
    metrics:
    - type: ndcg_at_1
      value: 15.443999999999999
    - type: ndcg_at_3
      value: 24.745
    - type: ndcg_at_5
      value: 28.560000000000002
    - type: ndcg_at_10
      value: 32.495000000000005
    - type: ndcg_at_20
      value: 35.226
    - type: ndcg_at_100
      value: 38.957
    - type: ndcg_at_1000
      value: 40.684
    - type: map_at_1
      value: 15.062000000000001
    - type: map_at_3
      value: 22.236
    - type: map_at_5
      value: 24.362000000000002
    - type: map_at_10
      value: 26.008
    - type: map_at_20
      value: 26.77
    - type: map_at_100
      value: 27.305
    - type: map_at_1000
      value: 27.372999999999998
    - type: recall_at_1
      value: 15.062000000000001
    - type: recall_at_3
      value: 31.556
    - type: recall_at_5
      value: 40.705999999999996
    - type: recall_at_10
      value: 52.72
    - type: recall_at_20
      value: 63.336000000000006
    - type: recall_at_100
      value: 83.006
    - type: recall_at_1000
      value: 96.263
    - type: precision_at_1
      value: 15.443999999999999
    - type: precision_at_3
      value: 10.86
    - type: precision_at_5
      value: 8.441
    - type: precision_at_10
      value: 5.486
    - type: precision_at_20
      value: 3.308
    - type: precision_at_100
      value: 0.8750000000000001
    - type: precision_at_1000
      value: 0.10200000000000001
    - type: mrr_at_1
      value: 15.444099999999999
    - type: mrr_at_3
      value: 22.7006
    - type: mrr_at_5
      value: 24.843799999999998
    - type: mrr_at_10
      value: 26.458199999999998
    - type: mrr_at_20
      value: 27.2124
    - type: mrr_at_100
      value: 27.7184
    - type: mrr_at_1000
      value: 27.7802
    - type: nauc_ndcg_at_1_max
      value: 1.9339
    - type: nauc_ndcg_at_1_std
      value: -13.125200000000001
    - type: nauc_ndcg_at_1_diff1
      value: 30.440499999999997
    - type: nauc_ndcg_at_3_max
      value: 2.0631
    - type: nauc_ndcg_at_3_std
      value: -15.065600000000002
    - type: nauc_ndcg_at_3_diff1
      value: 25.459300000000002
    - type: nauc_ndcg_at_5_max
      value: 2.7612
    - type: nauc_ndcg_at_5_std
      value: -15.576400000000001
    - type: nauc_ndcg_at_5_diff1
      value: 24.861
    - type: nauc_ndcg_at_10_max
      value: 3.5461
    - type: nauc_ndcg_at_10_std
      value: -15.2368
    - type: nauc_ndcg_at_10_diff1
      value: 25.328699999999998
    - type: nauc_ndcg_at_20_max
      value: 4.4956000000000005
    - type: nauc_ndcg_at_20_std
      value: -13.415099999999999
    - type: nauc_ndcg_at_20_diff1
      value: 25.401200000000003
    - type: nauc_ndcg_at_100_max
      value: 5.1996
    - type: nauc_ndcg_at_100_std
      value: -10.7691
    - type: nauc_ndcg_at_100_diff1
      value: 25.4837
    - type: nauc_ndcg_at_1000_max
      value: 4.8437
    - type: nauc_ndcg_at_1000_std
      value: -11.6759
    - type: nauc_ndcg_at_1000_diff1
      value: 25.6542
    - type: nauc_map_at_1_max
      value: 1.8748999999999998
    - type: nauc_map_at_1_std
      value: -13.203000000000001
    - type: nauc_map_at_1_diff1
      value: 30.786599999999996
    - type: nauc_map_at_3_max
      value: 1.9382
    - type: nauc_map_at_3_std
      value: -14.772499999999999
    - type: nauc_map_at_3_diff1
      value: 26.579900000000002
    - type: nauc_map_at_5_max
      value: 2.3708
    - type: nauc_map_at_5_std
      value: -15.093300000000001
    - type: nauc_map_at_5_diff1
      value: 26.2289
    - type: nauc_map_at_10_max
      value: 2.7201
    - type: nauc_map_at_10_std
      value: -14.9842
    - type: nauc_map_at_10_diff1
      value: 26.431700000000003
    - type: nauc_map_at_20_max
      value: 2.9757
    - type: nauc_map_at_20_std
      value: -14.4729
    - type: nauc_map_at_20_diff1
      value: 26.4573
    - type: nauc_map_at_100_max
      value: 3.0642
    - type: nauc_map_at_100_std
      value: -14.1146
    - type: nauc_map_at_100_diff1
      value: 26.472
    - type: nauc_map_at_1000_max
      value: 3.0554
    - type: nauc_map_at_1000_std
      value: -14.1365
    - type: nauc_map_at_1000_diff1
      value: 26.477899999999998
    - type: nauc_recall_at_1_max
      value: 1.8748999999999998
    - type: nauc_recall_at_1_std
      value: -13.203000000000001
    - type: nauc_recall_at_1_diff1
      value: 30.786599999999996
    - type: nauc_recall_at_3_max
      value: 2.2464999999999997
    - type: nauc_recall_at_3_std
      value: -15.7745
    - type: nauc_recall_at_3_diff1
      value: 22.8494
    - type: nauc_recall_at_5_max
      value: 3.5999999999999996
    - type: nauc_recall_at_5_std
      value: -16.7106
    - type: nauc_recall_at_5_diff1
      value: 21.6902
    - type: nauc_recall_at_10_max
      value: 5.6766
    - type: nauc_recall_at_10_std
      value: -15.768699999999999
    - type: nauc_recall_at_10_diff1
      value: 22.658900000000003
    - type: nauc_recall_at_20_max
      value: 9.5641
    - type: nauc_recall_at_20_std
      value: -8.8567
    - type: nauc_recall_at_20_diff1
      value: 22.6219
    - type: nauc_recall_at_100_max
      value: 19.2898
    - type: nauc_recall_at_100_std
      value: 17.354400000000002
    - type: nauc_recall_at_100_diff1
      value: 21.6465
    - type: nauc_recall_at_1000_max
      value: 43.4838
    - type: nauc_recall_at_1000_std
      value: 57.456300000000006
    - type: nauc_recall_at_1000_diff1
      value: 19.6644
    - type: nauc_precision_at_1_max
      value: 1.9339
    - type: nauc_precision_at_1_std
      value: -13.125200000000001
    - type: nauc_precision_at_1_diff1
      value: 30.440499999999997
    - type: nauc_precision_at_3_max
      value: 2.1921
    - type: nauc_precision_at_3_std
      value: -15.8918
    - type: nauc_precision_at_3_diff1
      value: 22.609099999999998
    - type: nauc_precision_at_5_max
      value: 3.8808000000000002
    - type: nauc_precision_at_5_std
      value: -16.6817
    - type: nauc_precision_at_5_diff1
      value: 21.0081
    - type: nauc_precision_at_10_max
      value: 6.2251
    - type: nauc_precision_at_10_std
      value: -14.9695
    - type: nauc_precision_at_10_diff1
      value: 21.3706
    - type: nauc_precision_at_20_max
      value: 10.3311
    - type: nauc_precision_at_20_std
      value: -7.5957
    - type: nauc_precision_at_20_diff1
      value: 20.4241
    - type: nauc_precision_at_100_max
      value: 18.7934
    - type: nauc_precision_at_100_std
      value: 16.6688
    - type: nauc_precision_at_100_diff1
      value: 13.4334
    - type: nauc_precision_at_1000_max
      value: 22.3609
    - type: nauc_precision_at_1000_std
      value: 22.090799999999998
    - type: nauc_precision_at_1000_diff1
      value: -1.5147000000000002
    - type: nauc_mrr_at_1_max
      value: 1.9339
    - type: nauc_mrr_at_1_std
      value: -13.125200000000001
    - type: nauc_mrr_at_1_diff1
      value: 30.440499999999997
    - type: nauc_mrr_at_3_max
      value: 2.0884
    - type: nauc_mrr_at_3_std
      value: -14.5665
    - type: nauc_mrr_at_3_diff1
      value: 26.270100000000003
    - type: nauc_mrr_at_5_max
      value: 2.5026
    - type: nauc_mrr_at_5_std
      value: -14.8794
    - type: nauc_mrr_at_5_diff1
      value: 25.8982
    - type: nauc_mrr_at_10_max
      value: 2.8118
    - type: nauc_mrr_at_10_std
      value: -14.7608
    - type: nauc_mrr_at_10_diff1
      value: 26.1961
    - type: nauc_mrr_at_20_max
      value: 3.0701
    - type: nauc_mrr_at_20_std
      value: -14.2605
    - type: nauc_mrr_at_20_diff1
      value: 26.206699999999998
    - type: nauc_mrr_at_100_max
      value: 3.1292
    - type: nauc_mrr_at_100_std
      value: -13.9589
    - type: nauc_mrr_at_100_diff1
      value: 26.227099999999997
    - type: nauc_mrr_at_1000_max
      value: 3.1135
    - type: nauc_mrr_at_1000_std
      value: -13.9831
    - type: nauc_mrr_at_1000_diff1
      value: 26.234099999999998
    - type: main_score
      value: 32.495000000000005
    task:
      type: Retrieval
  - dataset:
      config: en
      name: MTEB MTOPDomainClassification (en)
      revision: d80d48c1eb48d3562165c59d59d0034df9fff0bf
      split: test
      type: mteb/mtop_domain
    metrics:
    - type: accuracy
      value: 91.31099999999999
    - type: f1
      value: 90.9331
    - type: f1_weighted
      value: 91.2787
    - type: main_score
      value: 91.31099999999999
    task:
      type: Classification
  - dataset:
      config: en
      name: MTEB MTOPIntentClassification (en)
      revision: ae001d0e6b1228650b7bd1c2c65fb50ad11a8aba
      split: test
      type: mteb/mtop_intent
    metrics:
    - type: accuracy
      value: 54.9362
    - type: f1
      value: 38.364399999999996
    - type: f1_weighted
      value: 57.1133
    - type: main_score
      value: 54.9362
    task:
      type: Classification
  - dataset:
      config: en
      name: MTEB MassiveIntentClassification (en)
      revision: 4672e20407010da34463acc759c162ca9734bca6
      split: test
      type: mteb/amazon_massive_intent
    metrics:
    - type: accuracy
      value: 64.5461
    - type: f1
      value: 60.8751
    - type: f1_weighted
      value: 63.248599999999996
    - type: main_score
      value: 64.5461
    task:
      type: Classification
  - dataset:
      config: en
      name: MTEB MassiveScenarioClassification (en)
      revision: fad2c6e8459f9e1c45d9315f4953d921437d70f8
      split: test
      type: mteb/amazon_massive_scenario
    metrics:
    - type: accuracy
      value: 71.6476
    - type: f1
      value: 71.03110000000001
    - type: f1_weighted
      value: 71.3832
    - type: main_score
      value: 71.6476
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB MedrxivClusteringP2P (default)
      revision: e7a26af6f3ae46b30dde8737f02c07b1505bcc73
      split: test
      type: mteb/medrxiv-clustering-p2p
    metrics:
    - type: v_measure
      value: 32.3037
    - type: v_measure_std
      value: 1.4981
    - type: main_score
      value: 32.3037
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB MedrxivClusteringS2S (default)
      revision: 35191c8c0dca72d8ff3efcd72aa802307d469663
      split: test
      type: mteb/medrxiv-clustering-s2s
    metrics:
    - type: v_measure
      value: 31.9128
    - type: v_measure_std
      value: 1.4597
    - type: main_score
      value: 31.9128
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB MindSmallReranking (default)
      revision: 59042f120c80e8afa9cdbb224f67076cec0fc9a7
      split: test
      type: mteb/mind_small
    metrics:
    - type: map
      value: 32.2181
    - type: mrr
      value: 33.4843
    - type: nAUC_map_max
      value: -17.8061
    - type: nAUC_map_std
      value: -1.1424
    - type: nAUC_map_diff1
      value: 14.106
    - type: nAUC_mrr_max
      value: -12.6864
    - type: nAUC_mrr_std
      value: 0.7633
    - type: nAUC_mrr_diff1
      value: 13.168099999999999
    - type: main_score
      value: 32.2181
    task:
      type: Reranking
  - dataset:
      config: default
      name: MTEB NFCorpus (default)
      revision: ec0fa4fe99da2ff19ca1214b7966684033a58814
      split: test
      type: mteb/nfcorpus
    metrics:
    - type: ndcg_at_1
      value: 45.356
    - type: ndcg_at_3
      value: 42.643
    - type: ndcg_at_5
      value: 40.882000000000005
    - type: ndcg_at_10
      value: 37.25
    - type: ndcg_at_20
      value: 34.863
    - type: ndcg_at_100
      value: 34.496
    - type: ndcg_at_1000
      value: 43.374
    - type: map_at_1
      value: 6.126
    - type: map_at_3
      value: 10.301
    - type: map_at_5
      value: 12.084999999999999
    - type: map_at_10
      value: 14.152000000000001
    - type: map_at_20
      value: 15.796
    - type: map_at_100
      value: 18.27
    - type: map_at_1000
      value: 19.88
    - type: recall_at_1
      value: 6.126
    - type: recall_at_3
      value: 11.706
    - type: recall_at_5
      value: 14.419
    - type: recall_at_10
      value: 18.427
    - type: recall_at_20
      value: 22.7
    - type: recall_at_100
      value: 35.018
    - type: recall_at_1000
      value: 67.66
    - type: precision_at_1
      value: 47.368
    - type: precision_at_3
      value: 40.144000000000005
    - type: precision_at_5
      value: 35.913000000000004
    - type: precision_at_10
      value: 27.74
    - type: precision_at_20
      value: 20.619
    - type: precision_at_100
      value: 9.071
    - type: precision_at_1000
      value: 2.226
    - type: mrr_at_1
      value: 47.678
    - type: mrr_at_3
      value: 55.1084
    - type: mrr_at_5
      value: 56.145500000000006
    - type: mrr_at_10
      value: 56.7134
    - type: mrr_at_20
      value: 57.0095
    - type: mrr_at_100
      value: 57.2211
    - type: mrr_at_1000
      value: 57.2755
    - type: nauc_ndcg_at_1_max
      value: 39.442899999999995
    - type: nauc_ndcg_at_1_std
      value: 25.1396
    - type: nauc_ndcg_at_1_diff1
      value: 35.5228
    - type: nauc_ndcg_at_3_max
      value: 42.536699999999996
    - type: nauc_ndcg_at_3_std
      value: 30.7104
    - type: nauc_ndcg_at_3_diff1
      value: 26.383699999999997
    - type: nauc_ndcg_at_5_max
      value: 44.2751
    - type: nauc_ndcg_at_5_std
      value: 31.6998
    - type: nauc_ndcg_at_5_diff1
      value: 24.4678
    - type: nauc_ndcg_at_10_max
      value: 41.806599999999996
    - type: nauc_ndcg_at_10_std
      value: 32.7977
    - type: nauc_ndcg_at_10_diff1
      value: 20.0545
    - type: nauc_ndcg_at_20_max
      value: 39.0588
    - type: nauc_ndcg_at_20_std
      value: 31.5545
    - type: nauc_ndcg_at_20_diff1
      value: 18.075499999999998
    - type: nauc_ndcg_at_100_max
      value: 40.562599999999996
    - type: nauc_ndcg_at_100_std
      value: 34.0612
    - type: nauc_ndcg_at_100_diff1
      value: 21.0169
    - type: nauc_ndcg_at_1000_max
      value: 46.1599
    - type: nauc_ndcg_at_1000_std
      value: 38.1991
    - type: nauc_ndcg_at_1000_diff1
      value: 21.7529
    - type: nauc_map_at_1_max
      value: 2.822
    - type: nauc_map_at_1_std
      value: -13.824200000000001
    - type: nauc_map_at_1_diff1
      value: 43.4619
    - type: nauc_map_at_3_max
      value: 10.7749
    - type: nauc_map_at_3_std
      value: -7.7192
    - type: nauc_map_at_3_diff1
      value: 33.543099999999995
    - type: nauc_map_at_5_max
      value: 15.534
    - type: nauc_map_at_5_std
      value: -4.6368
    - type: nauc_map_at_5_diff1
      value: 31.472499999999997
    - type: nauc_map_at_10_max
      value: 19.6203
    - type: nauc_map_at_10_std
      value: 0.9646
    - type: nauc_map_at_10_diff1
      value: 26.763199999999998
    - type: nauc_map_at_20_max
      value: 22.9019
    - type: nauc_map_at_20_std
      value: 5.4963999999999995
    - type: nauc_map_at_20_diff1
      value: 23.5639
    - type: nauc_map_at_100_max
      value: 26.9211
    - type: nauc_map_at_100_std
      value: 13.7679
    - type: nauc_map_at_100_diff1
      value: 21.4205
    - type: nauc_map_at_1000_max
      value: 27.795199999999998
    - type: nauc_map_at_1000_std
      value: 17.5388
    - type: nauc_map_at_1000_diff1
      value: 20.6324
    - type: nauc_recall_at_1_max
      value: 2.822
    - type: nauc_recall_at_1_std
      value: -13.824200000000001
    - type: nauc_recall_at_1_diff1
      value: 43.4619
    - type: nauc_recall_at_3_max
      value: 11.128499999999999
    - type: nauc_recall_at_3_std
      value: -6.583500000000001
    - type: nauc_recall_at_3_diff1
      value: 31.2104
    - type: nauc_recall_at_5_max
      value: 15.5377
    - type: nauc_recall_at_5_std
      value: -4.0625
    - type: nauc_recall_at_5_diff1
      value: 28.746199999999998
    - type: nauc_recall_at_10_max
      value: 17.7947
    - type: nauc_recall_at_10_std
      value: 1.9115
    - type: nauc_recall_at_10_diff1
      value: 20.028000000000002
    - type: nauc_recall_at_20_max
      value: 18.5316
    - type: nauc_recall_at_20_std
      value: 4.5177000000000005
    - type: nauc_recall_at_20_diff1
      value: 14.4906
    - type: nauc_recall_at_100_max
      value: 27.871299999999998
    - type: nauc_recall_at_100_std
      value: 22.9259
    - type: nauc_recall_at_100_diff1
      value: 12.8091
    - type: nauc_recall_at_1000_max
      value: 24.782899999999998
    - type: nauc_recall_at_1000_std
      value: 23.6364
    - type: nauc_recall_at_1000_diff1
      value: 8.318100000000001
    - type: nauc_precision_at_1_max
      value: 41.779500000000006
    - type: nauc_precision_at_1_std
      value: 25.690600000000003
    - type: nauc_precision_at_1_diff1
      value: 35.6552
    - type: nauc_precision_at_3_max
      value: 46.0167
    - type: nauc_precision_at_3_std
      value: 37.0565
    - type: nauc_precision_at_3_diff1
      value: 16.6278
    - type: nauc_precision_at_5_max
      value: 47.2631
    - type: nauc_precision_at_5_std
      value: 39.6181
    - type: nauc_precision_at_5_diff1
      value: 9.3291
    - type: nauc_precision_at_10_max
      value: 42.9477
    - type: nauc_precision_at_10_std
      value: 44.7365
    - type: nauc_precision_at_10_diff1
      value: -0.2033
    - type: nauc_precision_at_20_max
      value: 37.0473
    - type: nauc_precision_at_20_std
      value: 46.609
    - type: nauc_precision_at_20_diff1
      value: -5.4761999999999995
    - type: nauc_precision_at_100_max
      value: 24.1237
    - type: nauc_precision_at_100_std
      value: 49.1772
    - type: nauc_precision_at_100_diff1
      value: -6.9049
    - type: nauc_precision_at_1000_max
      value: 9.0734
    - type: nauc_precision_at_1000_std
      value: 38.4405
    - type: nauc_precision_at_1000_diff1
      value: -4.3116
    - type: nauc_mrr_at_1_max
      value: 41.5105
    - type: nauc_mrr_at_1_std
      value: 25.404500000000002
    - type: nauc_mrr_at_1_diff1
      value: 34.8177
    - type: nauc_mrr_at_3_max
      value: 47.332
    - type: nauc_mrr_at_3_std
      value: 33.2771
    - type: nauc_mrr_at_3_diff1
      value: 34.5929
    - type: nauc_mrr_at_5_max
      value: 48.044799999999995
    - type: nauc_mrr_at_5_std
      value: 33.596
    - type: nauc_mrr_at_5_diff1
      value: 34.4048
    - type: nauc_mrr_at_10_max
      value: 48.2427
    - type: nauc_mrr_at_10_std
      value: 33.9279
    - type: nauc_mrr_at_10_diff1
      value: 33.974900000000005
    - type: nauc_mrr_at_20_max
      value: 48.2093
    - type: nauc_mrr_at_20_std
      value: 33.9138
    - type: nauc_mrr_at_20_diff1
      value: 34.0267
    - type: nauc_mrr_at_100_max
      value: 48.322700000000005
    - type: nauc_mrr_at_100_std
      value: 34.096
    - type: nauc_mrr_at_100_diff1
      value: 34.1172
    - type: nauc_mrr_at_1000_max
      value: 48.2719
    - type: nauc_mrr_at_1000_std
      value: 34.034
    - type: nauc_mrr_at_1000_diff1
      value: 34.0978
    - type: main_score
      value: 37.25
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB NQ (default)
      revision: b774495ed302d8c44a3a7ea25c90dbce03968f31
      split: test
      type: mteb/nq
    metrics:
    - type: ndcg_at_1
      value: 37.254
    - type: ndcg_at_3
      value: 49.219
    - type: ndcg_at_5
      value: 54.037
    - type: ndcg_at_10
      value: 58.044
    - type: ndcg_at_20
      value: 59.946999999999996
    - type: ndcg_at_100
      value: 61.61299999999999
    - type: ndcg_at_1000
      value: 62.046
    - type: map_at_1
      value: 33.053
    - type: map_at_3
      value: 44.91
    - type: map_at_5
      value: 47.83
    - type: map_at_10
      value: 49.739
    - type: map_at_20
      value: 50.336999999999996
    - type: map_at_100
      value: 50.626000000000005
    - type: map_at_1000
      value: 50.647
    - type: recall_at_1
      value: 33.053
    - type: recall_at_3
      value: 58.157000000000004
    - type: recall_at_5
      value: 69.235
    - type: recall_at_10
      value: 80.76
    - type: recall_at_20
      value: 87.756
    - type: recall_at_100
      value: 95.86200000000001
    - type: recall_at_1000
      value: 99.044
    - type: precision_at_1
      value: 37.254
    - type: precision_at_3
      value: 22.538
    - type: precision_at_5
      value: 16.344
    - type: precision_at_10
      value: 9.655
    - type: precision_at_20
      value: 5.2909999999999995
    - type: precision_at_100
      value: 1.167
    - type: precision_at_1000
      value: 0.121
    - type: mrr_at_1
      value: 37.2538
    - type: mrr_at_3
      value: 48.4453
    - type: mrr_at_5
      value: 50.8338
    - type: mrr_at_10
      value: 52.221700000000006
    - type: mrr_at_20
      value: 52.660399999999996
    - type: mrr_at_100
      value: 52.85490000000001
    - type: mrr_at_1000
      value: 52.869299999999996
    - type: nauc_ndcg_at_1_max
      value: 22.453400000000002
    - type: nauc_ndcg_at_1_std
      value: 1.3625
    - type: nauc_ndcg_at_1_diff1
      value: 33.4465
    - type: nauc_ndcg_at_3_max
      value: 29.2215
    - type: nauc_ndcg_at_3_std
      value: 1.496
    - type: nauc_ndcg_at_3_diff1
      value: 28.881600000000002
    - type: nauc_ndcg_at_5_max
      value: 30.8294
    - type: nauc_ndcg_at_5_std
      value: 3.0327
    - type: nauc_ndcg_at_5_diff1
      value: 27.2679
    - type: nauc_ndcg_at_10_max
      value: 32.5349
    - type: nauc_ndcg_at_10_std
      value: 5.074
    - type: nauc_ndcg_at_10_diff1
      value: 26.9574
    - type: nauc_ndcg_at_20_max
      value: 32.2817
    - type: nauc_ndcg_at_20_std
      value: 5.8412
    - type: nauc_ndcg_at_20_diff1
      value: 27.62
    - type: nauc_ndcg_at_100_max
      value: 31.084
    - type: nauc_ndcg_at_100_std
      value: 5.8699
    - type: nauc_ndcg_at_100_diff1
      value: 28.0961
    - type: nauc_ndcg_at_1000_max
      value: 30.3847
    - type: nauc_ndcg_at_1000_std
      value: 4.9963
    - type: nauc_ndcg_at_1000_diff1
      value: 28.4336
    - type: nauc_map_at_1_max
      value: 20.5816
    - type: nauc_map_at_1_std
      value: -1.0661
    - type: nauc_map_at_1_diff1
      value: 33.6828
    - type: nauc_map_at_3_max
      value: 27.4552
    - type: nauc_map_at_3_std
      value: 0.769
    - type: nauc_map_at_3_diff1
      value: 30.0372
    - type: nauc_map_at_5_max
      value: 28.315099999999997
    - type: nauc_map_at_5_std
      value: 1.6410999999999998
    - type: nauc_map_at_5_diff1
      value: 29.2099
    - type: nauc_map_at_10_max
      value: 28.969299999999997
    - type: nauc_map_at_10_std
      value: 2.5593999999999997
    - type: nauc_map_at_10_diff1
      value: 29.0818
    - type: nauc_map_at_20_max
      value: 28.902299999999997
    - type: nauc_map_at_20_std
      value: 2.788
    - type: nauc_map_at_20_diff1
      value: 29.2439
    - type: nauc_map_at_100_max
      value: 28.7275
    - type: nauc_map_at_100_std
      value: 2.8171
    - type: nauc_map_at_100_diff1
      value: 29.313899999999997
    - type: nauc_map_at_1000_max
      value: 28.701
    - type: nauc_map_at_1000_std
      value: 2.7868
    - type: nauc_map_at_1000_diff1
      value: 29.3304
    - type: nauc_recall_at_1_max
      value: 20.5816
    - type: nauc_recall_at_1_std
      value: -1.0661
    - type: nauc_recall_at_1_diff1
      value: 33.6828
    - type: nauc_recall_at_3_max
      value: 33.0999
    - type: nauc_recall_at_3_std
      value: 1.5433000000000001
    - type: nauc_recall_at_3_diff1
      value: 24.7191
    - type: nauc_recall_at_5_max
      value: 38.3028
    - type: nauc_recall_at_5_std
      value: 5.4908
    - type: nauc_recall_at_5_diff1
      value: 19.3777
    - type: nauc_recall_at_10_max
      value: 49.9754
    - type: nauc_recall_at_10_std
      value: 15.2697
    - type: nauc_recall_at_10_diff1
      value: 15.338199999999999
    - type: nauc_recall_at_20_max
      value: 57.0007
    - type: nauc_recall_at_20_std
      value: 25.9537
    - type: nauc_recall_at_20_diff1
      value: 16.1382
    - type: nauc_recall_at_100_max
      value: 70.0766
    - type: nauc_recall_at_100_std
      value: 60.529599999999995
    - type: nauc_recall_at_100_diff1
      value: 12.1256
    - type: nauc_recall_at_1000_max
      value: 70.6831
    - type: nauc_recall_at_1000_std
      value: 73.87599999999999
    - type: nauc_recall_at_1000_diff1
      value: 18.0994
    - type: nauc_precision_at_1_max
      value: 22.453400000000002
    - type: nauc_precision_at_1_std
      value: 1.3625
    - type: nauc_precision_at_1_diff1
      value: 33.4465
    - type: nauc_precision_at_3_max
      value: 32.461
    - type: nauc_precision_at_3_std
      value: 6.0438
    - type: nauc_precision_at_3_diff1
      value: 19.4828
    - type: nauc_precision_at_5_max
      value: 30.8773
    - type: nauc_precision_at_5_std
      value: 9.5136
    - type: nauc_precision_at_5_diff1
      value: 10.8131
    - type: nauc_precision_at_10_max
      value: 28.0383
    - type: nauc_precision_at_10_std
      value: 15.0419
    - type: nauc_precision_at_10_diff1
      value: 2.5906
    - type: nauc_precision_at_20_max
      value: 22.5558
    - type: nauc_precision_at_20_std
      value: 18.2138
    - type: nauc_precision_at_20_diff1
      value: -0.5902000000000001
    - type: nauc_precision_at_100_max
      value: 9.1213
    - type: nauc_precision_at_100_std
      value: 18.0878
    - type: nauc_precision_at_100_diff1
      value: -6.768299999999999
    - type: nauc_precision_at_1000_max
      value: 1.3558000000000001
    - type: nauc_precision_at_1000_std
      value: 12.4464
    - type: nauc_precision_at_1000_diff1
      value: -7.8355999999999995
    - type: nauc_mrr_at_1_max
      value: 22.453400000000002
    - type: nauc_mrr_at_1_std
      value: 1.3625
    - type: nauc_mrr_at_1_diff1
      value: 33.4465
    - type: nauc_mrr_at_3_max
      value: 27.747100000000003
    - type: nauc_mrr_at_3_std
      value: 2.8298
    - type: nauc_mrr_at_3_diff1
      value: 29.8467
    - type: nauc_mrr_at_5_max
      value: 28.3625
    - type: nauc_mrr_at_5_std
      value: 3.5815
    - type: nauc_mrr_at_5_diff1
      value: 29.009
    - type: nauc_mrr_at_10_max
      value: 28.769699999999997
    - type: nauc_mrr_at_10_std
      value: 4.1444
    - type: nauc_mrr_at_10_diff1
      value: 29.0508
    - type: nauc_mrr_at_20_max
      value: 28.6226
    - type: nauc_mrr_at_20_std
      value: 4.2112
    - type: nauc_mrr_at_20_diff1
      value: 29.2674
    - type: nauc_mrr_at_100_max
      value: 28.4889
    - type: nauc_mrr_at_100_std
      value: 4.197900000000001
    - type: nauc_mrr_at_100_diff1
      value: 29.3558
    - type: nauc_mrr_at_1000_max
      value: 28.4672
    - type: nauc_mrr_at_1000_std
      value: 4.1723
    - type: nauc_mrr_at_1000_diff1
      value: 29.3661
    - type: main_score
      value: 58.044
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB QuoraRetrieval (default)
      revision: e4e08e0b7dbe3c8700f0daef558ff32256715259
      split: test
      type: mteb/quora
    metrics:
    - type: ndcg_at_1
      value: 80.65
    - type: ndcg_at_3
      value: 84.897
    - type: ndcg_at_5
      value: 86.545
    - type: ndcg_at_10
      value: 87.822
    - type: ndcg_at_20
      value: 88.51299999999999
    - type: ndcg_at_100
      value: 89.091
    - type: ndcg_at_1000
      value: 89.203
    - type: map_at_1
      value: 70.05799999999999
    - type: map_at_3
      value: 81.03399999999999
    - type: map_at_5
      value: 82.922
    - type: map_at_10
      value: 84.009
    - type: map_at_20
      value: 84.442
    - type: map_at_100
      value: 84.661
    - type: map_at_1000
      value: 84.679
    - type: recall_at_1
      value: 70.05799999999999
    - type: recall_at_3
      value: 86.763
    - type: recall_at_5
      value: 91.396
    - type: recall_at_10
      value: 95.148
    - type: recall_at_20
      value: 97.34
    - type: recall_at_100
      value: 99.47399999999999
    - type: recall_at_1000
      value: 99.977
    - type: precision_at_1
      value: 80.65
    - type: precision_at_3
      value: 37.15
    - type: precision_at_5
      value: 24.48
    - type: precision_at_10
      value: 13.347000000000001
    - type: precision_at_20
      value: 7.095
    - type: precision_at_100
      value: 1.5270000000000001
    - type: precision_at_1000
      value: 0.157
    - type: mrr_at_1
      value: 80.64
    - type: mrr_at_3
      value: 85.9483
    - type: mrr_at_5
      value: 86.6738
    - type: mrr_at_10
      value: 86.9798
    - type: mrr_at_20
      value: 87.06009999999999
    - type: mrr_at_100
      value: 87.08829999999999
    - type: mrr_at_1000
      value: 87.08930000000001
    - type: nauc_ndcg_at_1_max
      value: 37.1678
    - type: nauc_ndcg_at_1_std
      value: -33.5588
    - type: nauc_ndcg_at_1_diff1
      value: 77.2101
    - type: nauc_ndcg_at_3_max
      value: 35.085
    - type: nauc_ndcg_at_3_std
      value: -39.8447
    - type: nauc_ndcg_at_3_diff1
      value: 75.7084
    - type: nauc_ndcg_at_5_max
      value: 36.0947
    - type: nauc_ndcg_at_5_std
      value: -40.3617
    - type: nauc_ndcg_at_5_diff1
      value: 76.5872
    - type: nauc_ndcg_at_10_max
      value: 36.091899999999995
    - type: nauc_ndcg_at_10_std
      value: -39.8878
    - type: nauc_ndcg_at_10_diff1
      value: 76.5282
    - type: nauc_ndcg_at_20_max
      value: 36.6226
    - type: nauc_ndcg_at_20_std
      value: -38.3337
    - type: nauc_ndcg_at_20_diff1
      value: 76.4084
    - type: nauc_ndcg_at_100_max
      value: 36.9855
    - type: nauc_ndcg_at_100_std
      value: -36.561
    - type: nauc_ndcg_at_100_diff1
      value: 76.21860000000001
    - type: nauc_ndcg_at_1000_max
      value: 37.021300000000004
    - type: nauc_ndcg_at_1000_std
      value: -36.494
    - type: nauc_ndcg_at_1000_diff1
      value: 76.18599999999999
    - type: nauc_map_at_1_max
      value: 26.761000000000003
    - type: nauc_map_at_1_std
      value: -36.3749
    - type: nauc_map_at_1_diff1
      value: 80.0977
    - type: nauc_map_at_3_max
      value: 32.530300000000004
    - type: nauc_map_at_3_std
      value: -42.3896
    - type: nauc_map_at_3_diff1
      value: 77.1352
    - type: nauc_map_at_5_max
      value: 34.322599999999994
    - type: nauc_map_at_5_std
      value: -41.9927
    - type: nauc_map_at_5_diff1
      value: 77.1848
    - type: nauc_map_at_10_max
      value: 35.0744
    - type: nauc_map_at_10_std
      value: -40.8511
    - type: nauc_map_at_10_diff1
      value: 76.86319999999999
    - type: nauc_map_at_20_max
      value: 35.442299999999996
    - type: nauc_map_at_20_std
      value: -39.7228
    - type: nauc_map_at_20_diff1
      value: 76.67150000000001
    - type: nauc_map_at_100_max
      value: 35.5927
    - type: nauc_map_at_100_std
      value: -38.9448
    - type: nauc_map_at_100_diff1
      value: 76.57169999999999
    - type: nauc_map_at_1000_max
      value: 35.612100000000005
    - type: nauc_map_at_1000_std
      value: -38.8973
    - type: nauc_map_at_1000_diff1
      value: 76.5656
    - type: nauc_recall_at_1_max
      value: 26.761000000000003
    - type: nauc_recall_at_1_std
      value: -36.3749
    - type: nauc_recall_at_1_diff1
      value: 80.0977
    - type: nauc_recall_at_3_max
      value: 29.2557
    - type: nauc_recall_at_3_std
      value: -48.3412
    - type: nauc_recall_at_3_diff1
      value: 73.5986
    - type: nauc_recall_at_5_max
      value: 32.0708
    - type: nauc_recall_at_5_std
      value: -51.9846
    - type: nauc_recall_at_5_diff1
      value: 74.0073
    - type: nauc_recall_at_10_max
      value: 30.5549
    - type: nauc_recall_at_10_std
      value: -56.8778
    - type: nauc_recall_at_10_diff1
      value: 73.5398
    - type: nauc_recall_at_20_max
      value: 32.5741
    - type: nauc_recall_at_20_std
      value: -50.3935
    - type: nauc_recall_at_20_diff1
      value: 73.6634
    - type: nauc_recall_at_100_max
      value: 40.8872
    - type: nauc_recall_at_100_std
      value: -18.2413
    - type: nauc_recall_at_100_diff1
      value: 72.1894
    - type: nauc_recall_at_1000_max
      value: 31.5668
    - type: nauc_recall_at_1000_std
      value: 51.0679
    - type: nauc_recall_at_1000_diff1
      value: 59.485299999999995
    - type: nauc_precision_at_1_max
      value: 37.1678
    - type: nauc_precision_at_1_std
      value: -33.5588
    - type: nauc_precision_at_1_diff1
      value: 77.2101
    - type: nauc_precision_at_3_max
      value: 9.868
    - type: nauc_precision_at_3_std
      value: 4.8771
    - type: nauc_precision_at_3_diff1
      value: -16.2165
    - type: nauc_precision_at_5_max
      value: 5.169
    - type: nauc_precision_at_5_std
      value: 15.223700000000001
    - type: nauc_precision_at_5_diff1
      value: -29.328300000000002
    - type: nauc_precision_at_10_max
      value: 0.3411
    - type: nauc_precision_at_10_std
      value: 24.0866
    - type: nauc_precision_at_10_diff1
      value: -37.514399999999995
    - type: nauc_precision_at_20_max
      value: -1.981
    - type: nauc_precision_at_20_std
      value: 30.408099999999997
    - type: nauc_precision_at_20_diff1
      value: -41.1355
    - type: nauc_precision_at_100_max
      value: -4.2999
    - type: nauc_precision_at_100_std
      value: 36.4541
    - type: nauc_precision_at_100_diff1
      value: -43.7797
    - type: nauc_precision_at_1000_max
      value: -4.4928
    - type: nauc_precision_at_1000_std
      value: 36.9861
    - type: nauc_precision_at_1000_diff1
      value: -44.182
    - type: nauc_mrr_at_1_max
      value: 37.2354
    - type: nauc_mrr_at_1_std
      value: -33.4342
    - type: nauc_mrr_at_1_diff1
      value: 77.2283
    - type: nauc_mrr_at_3_max
      value: 38.000299999999996
    - type: nauc_mrr_at_3_std
      value: -34.9304
    - type: nauc_mrr_at_3_diff1
      value: 76.20280000000001
    - type: nauc_mrr_at_5_max
      value: 38.3135
    - type: nauc_mrr_at_5_std
      value: -34.707
    - type: nauc_mrr_at_5_diff1
      value: 76.4365
    - type: nauc_mrr_at_10_max
      value: 38.0013
    - type: nauc_mrr_at_10_std
      value: -34.6562
    - type: nauc_mrr_at_10_diff1
      value: 76.44069999999999
    - type: nauc_mrr_at_20_max
      value: 38.0368
    - type: nauc_mrr_at_20_std
      value: -34.4726
    - type: nauc_mrr_at_20_diff1
      value: 76.4482
    - type: nauc_mrr_at_100_max
      value: 38.0243
    - type: nauc_mrr_at_100_std
      value: -34.4696
    - type: nauc_mrr_at_100_diff1
      value: 76.4569
    - type: nauc_mrr_at_1000_max
      value: 38.0227
    - type: nauc_mrr_at_1000_std
      value: -34.4733
    - type: nauc_mrr_at_1000_diff1
      value: 76.45739999999999
    - type: main_score
      value: 87.822
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB RedditClustering (default)
      revision: 24640382cdbf8abc73003fb0fa6d111a705499eb
      split: test
      type: mteb/reddit-clustering
    metrics:
    - type: v_measure
      value: 54.4296
    - type: v_measure_std
      value: 5.026400000000001
    - type: main_score
      value: 54.4296
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB RedditClusteringP2P (default)
      revision: 385e3cb46b4cfa89021f56c4380204149d0efe33
      split: test
      type: mteb/reddit-clustering-p2p
    metrics:
    - type: v_measure
      value: 58.1919
    - type: v_measure_std
      value: 12.618199999999998
    - type: main_score
      value: 58.1919
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB SCIDOCS (default)
      revision: f8c2fcf00f625baaa80f62ec5bd9e1fff3b8ae88
      split: test
      type: mteb/scidocs
    metrics:
    - type: ndcg_at_1
      value: 28.1
    - type: ndcg_at_3
      value: 22.721
    - type: ndcg_at_5
      value: 20.015
    - type: ndcg_at_10
      value: 24.146
    - type: ndcg_at_20
      value: 27.74
    - type: ndcg_at_100
      value: 33.900000000000006
    - type: ndcg_at_1000
      value: 39.728
    - type: map_at_1
      value: 5.737
    - type: map_at_3
      value: 10.474
    - type: map_at_5
      value: 12.656
    - type: map_at_10
      value: 14.896
    - type: map_at_20
      value: 16.317999999999998
    - type: map_at_100
      value: 17.646
    - type: map_at_1000
      value: 18.029999999999998
    - type: recall_at_1
      value: 5.737
    - type: recall_at_3
      value: 12.897
    - type: recall_at_5
      value: 17.854999999999997
    - type: recall_at_10
      value: 25.4
    - type: recall_at_20
      value: 33.817
    - type: recall_at_100
      value: 53.772
    - type: recall_at_1000
      value: 82.013
    - type: precision_at_1
      value: 28.1
    - type: precision_at_3
      value: 21.2
    - type: precision_at_5
      value: 17.599999999999998
    - type: precision_at_10
      value: 12.540000000000001
    - type: precision_at_20
      value: 8.34
    - type: precision_at_100
      value: 2.651
    - type: precision_at_1000
      value: 0.404
    - type: mrr_at_1
      value: 28.1
    - type: mrr_at_3
      value: 35.9167
    - type: mrr_at_5
      value: 38.0967
    - type: mrr_at_10
      value: 39.578799999999994
    - type: mrr_at_20
      value: 40.2541
    - type: mrr_at_100
      value: 40.687
    - type: mrr_at_1000
      value: 40.722
    - type: nauc_ndcg_at_1_max
      value: 21.2698
    - type: nauc_ndcg_at_1_std
      value: 8.8522
    - type: nauc_ndcg_at_1_diff1
      value: 21.6443
    - type: nauc_ndcg_at_3_max
      value: 28.6762
    - type: nauc_ndcg_at_3_std
      value: 13.8129
    - type: nauc_ndcg_at_3_diff1
      value: 16.4517
    - type: nauc_ndcg_at_5_max
      value: 31.252000000000002
    - type: nauc_ndcg_at_5_std
      value: 17.3178
    - type: nauc_ndcg_at_5_diff1
      value: 16.8954
    - type: nauc_ndcg_at_10_max
      value: 32.581700000000005
    - type: nauc_ndcg_at_10_std
      value: 19.936300000000003
    - type: nauc_ndcg_at_10_diff1
      value: 17.086499999999997
    - type: nauc_ndcg_at_20_max
      value: 32.3902
    - type: nauc_ndcg_at_20_std
      value: 22.8215
    - type: nauc_ndcg_at_20_diff1
      value: 14.6836
    - type: nauc_ndcg_at_100_max
      value: 33.2665
    - type: nauc_ndcg_at_100_std
      value: 28.93
    - type: nauc_ndcg_at_100_diff1
      value: 14.8837
    - type: nauc_ndcg_at_1000_max
      value: 32.9079
    - type: nauc_ndcg_at_1000_std
      value: 28.228900000000003
    - type: nauc_ndcg_at_1000_diff1
      value: 15.9599
    - type: nauc_map_at_1_max
      value: 20.3725
    - type: nauc_map_at_1_std
      value: 8.7546
    - type: nauc_map_at_1_diff1
      value: 20.8754
    - type: nauc_map_at_3_max
      value: 27.0845
    - type: nauc_map_at_3_std
      value: 12.6727
    - type: nauc_map_at_3_diff1
      value: 15.6365
    - type: nauc_map_at_5_max
      value: 29.2312
    - type: nauc_map_at_5_std
      value: 15.8701
    - type: nauc_map_at_5_diff1
      value: 15.891
    - type: nauc_map_at_10_max
      value: 30.3676
    - type: nauc_map_at_10_std
      value: 18.5848
    - type: nauc_map_at_10_diff1
      value: 15.155299999999999
    - type: nauc_map_at_20_max
      value: 30.6006
    - type: nauc_map_at_20_std
      value: 20.4984
    - type: nauc_map_at_20_diff1
      value: 13.8149
    - type: nauc_map_at_100_max
      value: 31.3216
    - type: nauc_map_at_100_std
      value: 22.8546
    - type: nauc_map_at_100_diff1
      value: 13.9657
    - type: nauc_map_at_1000_max
      value: 31.3095
    - type: nauc_map_at_1000_std
      value: 22.991
    - type: nauc_map_at_1000_diff1
      value: 13.999500000000001
    - type: nauc_recall_at_1_max
      value: 20.3725
    - type: nauc_recall_at_1_std
      value: 8.7546
    - type: nauc_recall_at_1_diff1
      value: 20.8754
    - type: nauc_recall_at_3_max
      value: 30.6276
    - type: nauc_recall_at_3_std
      value: 15.5861
    - type: nauc_recall_at_3_diff1
      value: 13.9652
    - type: nauc_recall_at_5_max
      value: 33.4455
    - type: nauc_recall_at_5_std
      value: 20.4822
    - type: nauc_recall_at_5_diff1
      value: 14.566799999999999
    - type: nauc_recall_at_10_max
      value: 33.9121
    - type: nauc_recall_at_10_std
      value: 23.4277
    - type: nauc_recall_at_10_diff1
      value: 14.5769
    - type: nauc_recall_at_20_max
      value: 30.939100000000003
    - type: nauc_recall_at_20_std
      value: 27.683400000000002
    - type: nauc_recall_at_20_diff1
      value: 8.519300000000001
    - type: nauc_recall_at_100_max
      value: 28.9221
    - type: nauc_recall_at_100_std
      value: 41.281600000000005
    - type: nauc_recall_at_100_diff1
      value: 7.3066
    - type: nauc_recall_at_1000_max
      value: 24.2406
    - type: nauc_recall_at_1000_std
      value: 43.2715
    - type: nauc_recall_at_1000_diff1
      value: 10.2232
    - type: nauc_precision_at_1_max
      value: 21.2698
    - type: nauc_precision_at_1_std
      value: 8.8522
    - type: nauc_precision_at_1_diff1
      value: 21.6443
    - type: nauc_precision_at_3_max
      value: 31.2776
    - type: nauc_precision_at_3_std
      value: 15.8911
    - type: nauc_precision_at_3_diff1
      value: 14.357800000000001
    - type: nauc_precision_at_5_max
      value: 34.034
    - type: nauc_precision_at_5_std
      value: 20.6595
    - type: nauc_precision_at_5_diff1
      value: 15.1316
    - type: nauc_precision_at_10_max
      value: 34.4474
    - type: nauc_precision_at_10_std
      value: 23.5843
    - type: nauc_precision_at_10_diff1
      value: 14.9385
    - type: nauc_precision_at_20_max
      value: 31.4376
    - type: nauc_precision_at_20_std
      value: 27.7123
    - type: nauc_precision_at_20_diff1
      value: 8.6083
    - type: nauc_precision_at_100_max
      value: 29.401300000000003
    - type: nauc_precision_at_100_std
      value: 40.5942
    - type: nauc_precision_at_100_diff1
      value: 7.6172
    - type: nauc_precision_at_1000_max
      value: 25.2832
    - type: nauc_precision_at_1000_std
      value: 40.9653
    - type: nauc_precision_at_1000_diff1
      value: 10.3534
    - type: nauc_mrr_at_1_max
      value: 21.2698
    - type: nauc_mrr_at_1_std
      value: 8.8522
    - type: nauc_mrr_at_1_diff1
      value: 21.6443
    - type: nauc_mrr_at_3_max
      value: 26.8557
    - type: nauc_mrr_at_3_std
      value: 12.482600000000001
    - type: nauc_mrr_at_3_diff1
      value: 19.3542
    - type: nauc_mrr_at_5_max
      value: 28.0333
    - type: nauc_mrr_at_5_std
      value: 13.4664
    - type: nauc_mrr_at_5_diff1
      value: 20.0372
    - type: nauc_mrr_at_10_max
      value: 28.0659
    - type: nauc_mrr_at_10_std
      value: 13.791999999999998
    - type: nauc_mrr_at_10_diff1
      value: 20.7022
    - type: nauc_mrr_at_20_max
      value: 27.886499999999998
    - type: nauc_mrr_at_20_std
      value: 13.952700000000002
    - type: nauc_mrr_at_20_diff1
      value: 20.5573
    - type: nauc_mrr_at_100_max
      value: 27.714299999999998
    - type: nauc_mrr_at_100_std
      value: 13.863700000000001
    - type: nauc_mrr_at_100_diff1
      value: 20.5074
    - type: nauc_mrr_at_1000_max
      value: 27.700599999999998
    - type: nauc_mrr_at_1000_std
      value: 13.8399
    - type: nauc_mrr_at_1000_diff1
      value: 20.5031
    - type: main_score
      value: 24.146
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB SICK-R (default)
      revision: 20a6d6f312dd54037fe07a32d58e5e168867909d
      split: test
      type: mteb/sickr-sts
    metrics:
    - type: pearson
      value: 78.6926
    - type: spearman
      value: 71.2001
    - type: cosine_pearson
      value: 78.6926
    - type: cosine_spearman
      value: 71.2001
    - type: manhattan_pearson
      value: 75.264
    - type: manhattan_spearman
      value: 71.1303
    - type: euclidean_pearson
      value: 75.3261
    - type: euclidean_spearman
      value: 71.2001
    - type: main_score
      value: 71.2001
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB STS12 (default)
      revision: a0d554a64d88156834ff5ae9920b964011b16384
      split: test
      type: mteb/sts12-sts
    metrics:
    - type: pearson
      value: 71.0057
    - type: spearman
      value: 65.9247
    - type: cosine_pearson
      value: 71.0057
    - type: cosine_spearman
      value: 65.9247
    - type: manhattan_pearson
      value: 67.392
    - type: manhattan_spearman
      value: 65.8026
    - type: euclidean_pearson
      value: 67.5888
    - type: euclidean_spearman
      value: 65.92479999999999
    - type: main_score
      value: 65.9247
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB STS13 (default)
      revision: 7e90230a92c190f1bf69ae9002b8cea547a64cca
      split: test
      type: mteb/sts13-sts
    metrics:
    - type: pearson
      value: 81.67649999999999
    - type: spearman
      value: 81.7525
    - type: cosine_pearson
      value: 81.67649999999999
    - type: cosine_spearman
      value: 81.7525
    - type: manhattan_pearson
      value: 81.0327
    - type: manhattan_spearman
      value: 81.6717
    - type: euclidean_pearson
      value: 81.10000000000001
    - type: euclidean_spearman
      value: 81.7526
    - type: main_score
      value: 81.7525
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB STS14 (default)
      revision: 6031580fec1f6af667f0bd2da0a551cf4f0b2375
      split: test
      type: mteb/sts14-sts
    metrics:
    - type: pearson
      value: 79.47579999999999
    - type: spearman
      value: 74.2305
    - type: cosine_pearson
      value: 79.47579999999999
    - type: cosine_spearman
      value: 74.2305
    - type: manhattan_pearson
      value: 77.8846
    - type: manhattan_spearman
      value: 74.1908
    - type: euclidean_pearson
      value: 77.9333
    - type: euclidean_spearman
      value: 74.2305
    - type: main_score
      value: 74.2305
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB STS15 (default)
      revision: ae752c7c21bf194d8b67fd573edf7ae58183cbe3
      split: test
      type: mteb/sts15-sts
    metrics:
    - type: pearson
      value: 82.90180000000001
    - type: spearman
      value: 84.1271
    - type: cosine_pearson
      value: 82.90180000000001
    - type: cosine_spearman
      value: 84.1271
    - type: manhattan_pearson
      value: 83.6431
    - type: manhattan_spearman
      value: 84.1091
    - type: euclidean_pearson
      value: 83.6388
    - type: euclidean_spearman
      value: 84.127
    - type: main_score
      value: 84.1271
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB STS16 (default)
      revision: 4d8694f8f0e0100860b497b999b3dbed754a0513
      split: test
      type: mteb/sts16-sts
    metrics:
    - type: pearson
      value: 80.19810000000001
    - type: spearman
      value: 81.6627
    - type: cosine_pearson
      value: 80.19810000000001
    - type: cosine_spearman
      value: 81.6627
    - type: manhattan_pearson
      value: 81.4605
    - type: manhattan_spearman
      value: 81.62819999999999
    - type: euclidean_pearson
      value: 81.5043
    - type: euclidean_spearman
      value: 81.6627
    - type: main_score
      value: 81.6627
    task:
      type: STS
  - dataset:
      config: en-de
      name: MTEB STS17 (en-de)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 47.9276
    - type: spearman
      value: 50.0286
    - type: cosine_pearson
      value: 47.9276
    - type: cosine_spearman
      value: 50.0286
    - type: manhattan_pearson
      value: 48.5188
    - type: manhattan_spearman
      value: 50.432
    - type: euclidean_pearson
      value: 48.1655
    - type: euclidean_spearman
      value: 50.0286
    - type: main_score
      value: 50.0286
    task:
      type: STS
  - dataset:
      config: en-tr
      name: MTEB STS17 (en-tr)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 24.4119
    - type: spearman
      value: 22.1195
    - type: cosine_pearson
      value: 24.4119
    - type: cosine_spearman
      value: 22.1195
    - type: manhattan_pearson
      value: 25.873800000000003
    - type: manhattan_spearman
      value: 23.6049
    - type: euclidean_pearson
      value: 24.3693
    - type: euclidean_spearman
      value: 22.1195
    - type: main_score
      value: 22.1195
    task:
      type: STS
  - dataset:
      config: en-ar
      name: MTEB STS17 (en-ar)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 22.656200000000002
    - type: spearman
      value: 22.5445
    - type: cosine_pearson
      value: 22.656200000000002
    - type: cosine_spearman
      value: 22.5445
    - type: manhattan_pearson
      value: 22.414
    - type: manhattan_spearman
      value: 22.1601
    - type: euclidean_pearson
      value: 22.7736
    - type: euclidean_spearman
      value: 22.5445
    - type: main_score
      value: 22.5445
    task:
      type: STS
  - dataset:
      config: nl-en
      name: MTEB STS17 (nl-en)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 44.4998
    - type: spearman
      value: 43.1984
    - type: cosine_pearson
      value: 44.4998
    - type: cosine_spearman
      value: 43.1984
    - type: manhattan_pearson
      value: 43.3837
    - type: manhattan_spearman
      value: 43.1122
    - type: euclidean_pearson
      value: 44.1642
    - type: euclidean_spearman
      value: 43.1984
    - type: main_score
      value: 43.1984
    task:
      type: STS
  - dataset:
      config: en-en
      name: MTEB STS17 (en-en)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 82.3891
    - type: spearman
      value: 83.9634
    - type: cosine_pearson
      value: 82.3891
    - type: cosine_spearman
      value: 83.9634
    - type: manhattan_pearson
      value: 83.1481
    - type: manhattan_spearman
      value: 83.9743
    - type: euclidean_pearson
      value: 83.2767
    - type: euclidean_spearman
      value: 83.9634
    - type: main_score
      value: 83.9634
    task:
      type: STS
  - dataset:
      config: it-en
      name: MTEB STS17 (it-en)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 35.3106
    - type: spearman
      value: 30.7572
    - type: cosine_pearson
      value: 35.3106
    - type: cosine_spearman
      value: 30.7572
    - type: manhattan_pearson
      value: 35.6552
    - type: manhattan_spearman
      value: 31.596000000000004
    - type: euclidean_pearson
      value: 35.4393
    - type: euclidean_spearman
      value: 30.7572
    - type: main_score
      value: 30.7572
    task:
      type: STS
  - dataset:
      config: es-en
      name: MTEB STS17 (es-en)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 36.9322
    - type: spearman
      value: 37.7137
    - type: cosine_pearson
      value: 36.9322
    - type: cosine_spearman
      value: 37.7137
    - type: manhattan_pearson
      value: 36.0714
    - type: manhattan_spearman
      value: 36.9979
    - type: euclidean_pearson
      value: 36.784800000000004
    - type: euclidean_spearman
      value: 37.7137
    - type: main_score
      value: 37.7137
    task:
      type: STS
  - dataset:
      config: fr-en
      name: MTEB STS17 (fr-en)
      revision: faeb762787bd10488a50c8b5be4a3b82e411949c
      split: test
      type: mteb/sts17-crosslingual-sts
    metrics:
    - type: pearson
      value: 39.963300000000004
    - type: spearman
      value: 38.9248
    - type: cosine_pearson
      value: 39.963300000000004
    - type: cosine_spearman
      value: 38.9248
    - type: manhattan_pearson
      value: 39.539699999999996
    - type: manhattan_spearman
      value: 38.191900000000004
    - type: euclidean_pearson
      value: 39.8596
    - type: euclidean_spearman
      value: 38.9248
    - type: main_score
      value: 38.9248
    task:
      type: STS
  - dataset:
      config: de-en
      name: MTEB STS22 (de-en)
      revision: de9d86b3b84231dc21f76c7b7af1f28e2f57f6e3
      split: test
      type: mteb/sts22-crosslingual-sts
    metrics:
    - type: pearson
      value: 56.0924
    - type: spearman
      value: 54.1844
    - type: cosine_pearson
      value: 56.0924
    - type: cosine_spearman
      value: 54.1844
    - type: manhattan_pearson
      value: 56.938100000000006
    - type: manhattan_spearman
      value: 53.9407
    - type: euclidean_pearson
      value: 57.9844
    - type: euclidean_spearman
      value: 54.1844
    - type: main_score
      value: 54.1844
    task:
      type: STS
  - dataset:
      config: en
      name: MTEB STS22 (en)
      revision: de9d86b3b84231dc21f76c7b7af1f28e2f57f6e3
      split: test
      type: mteb/sts22-crosslingual-sts
    metrics:
    - type: pearson
      value: 69.3771
    - type: spearman
      value: 69.3609
    - type: cosine_pearson
      value: 69.3771
    - type: cosine_spearman
      value: 69.3609
    - type: manhattan_pearson
      value: 70.8762
    - type: manhattan_spearman
      value: 69.1889
    - type: euclidean_pearson
      value: 70.9433
    - type: euclidean_spearman
      value: 69.3609
    - type: main_score
      value: 69.3609
    task:
      type: STS
  - dataset:
      config: pl-en
      name: MTEB STS22 (pl-en)
      revision: de9d86b3b84231dc21f76c7b7af1f28e2f57f6e3
      split: test
      type: mteb/sts22-crosslingual-sts
    metrics:
    - type: pearson
      value: 74.11609999999999
    - type: spearman
      value: 71.63340000000001
    - type: cosine_pearson
      value: 74.11609999999999
    - type: cosine_spearman
      value: 71.63340000000001
    - type: manhattan_pearson
      value: 73.2348
    - type: manhattan_spearman
      value: 71.1802
    - type: euclidean_pearson
      value: 73.284
    - type: euclidean_spearman
      value: 71.63340000000001
    - type: main_score
      value: 71.63340000000001
    task:
      type: STS
  - dataset:
      config: es-en
      name: MTEB STS22 (es-en)
      revision: de9d86b3b84231dc21f76c7b7af1f28e2f57f6e3
      split: test
      type: mteb/sts22-crosslingual-sts
    metrics:
    - type: pearson
      value: 70.08879999999999
    - type: spearman
      value: 73.79
    - type: cosine_pearson
      value: 70.08879999999999
    - type: cosine_spearman
      value: 73.79
    - type: manhattan_pearson
      value: 71.5415
    - type: manhattan_spearman
      value: 73.6588
    - type: euclidean_pearson
      value: 71.621
    - type: euclidean_spearman
      value: 73.79
    - type: main_score
      value: 73.79
    task:
      type: STS
  - dataset:
      config: zh-en
      name: MTEB STS22 (zh-en)
      revision: de9d86b3b84231dc21f76c7b7af1f28e2f57f6e3
      split: test
      type: mteb/sts22-crosslingual-sts
    metrics:
    - type: pearson
      value: 37.5935
    - type: spearman
      value: 39.5919
    - type: cosine_pearson
      value: 37.5935
    - type: cosine_spearman
      value: 39.5919
    - type: manhattan_pearson
      value: 37.1717
    - type: manhattan_spearman
      value: 38.6974
    - type: euclidean_pearson
      value: 37.5632
    - type: euclidean_spearman
      value: 39.5919
    - type: main_score
      value: 39.5919
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB STSBenchmark (default)
      revision: b0fddb56ed78048fa8b90373c8a3cfc37b684831
      split: test
      type: mteb/stsbenchmark-sts
    metrics:
    - type: pearson
      value: 79.9453
    - type: spearman
      value: 79.6569
    - type: cosine_pearson
      value: 79.9453
    - type: cosine_spearman
      value: 79.6569
    - type: manhattan_pearson
      value: 79.8923
    - type: manhattan_spearman
      value: 79.58370000000001
    - type: euclidean_pearson
      value: 79.9829
    - type: euclidean_spearman
      value: 79.6569
    - type: main_score
      value: 79.6569
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB SciDocsRR (default)
      revision: d3c5e1fc0b855ab6097bf1cda04dd73947d7caab
      split: test
      type: mteb/scidocs-reranking
    metrics:
    - type: map
      value: 88.09949999999999
    - type: mrr
      value: 96.6455
    - type: nAUC_map_max
      value: 53.3622
    - type: nAUC_map_std
      value: 70.3532
    - type: nAUC_map_diff1
      value: -0.21419999999999997
    - type: nAUC_mrr_max
      value: 88.893
    - type: nAUC_mrr_std
      value: 85.4516
    - type: nAUC_mrr_diff1
      value: 43.6847
    - type: main_score
      value: 88.09949999999999
    task:
      type: Reranking
  - dataset:
      config: default
      name: MTEB SciFact (default)
      revision: 0228b52cf27578f30900b9e5271d331663a030d7
      split: test
      type: mteb/scifact
    metrics:
    - type: ndcg_at_1
      value: 62.666999999999994
    - type: ndcg_at_3
      value: 69.77600000000001
    - type: ndcg_at_5
      value: 71.964
    - type: ndcg_at_10
      value: 74.72
    - type: ndcg_at_20
      value: 76.154
    - type: ndcg_at_100
      value: 76.961
    - type: ndcg_at_1000
      value: 77.294
    - type: map_at_1
      value: 60.011
    - type: map_at_3
      value: 67.135
    - type: map_at_5
      value: 68.78
    - type: map_at_10
      value: 70.101
    - type: map_at_20
      value: 70.56099999999999
    - type: map_at_100
      value: 70.687
    - type: map_at_1000
      value: 70.699
    - type: recall_at_1
      value: 60.011
    - type: recall_at_3
      value: 74.839
    - type: recall_at_5
      value: 80.028
    - type: recall_at_10
      value: 87.8
    - type: recall_at_20
      value: 93.10000000000001
    - type: recall_at_100
      value: 97.333
    - type: recall_at_1000
      value: 100.0
    - type: precision_at_1
      value: 62.666999999999994
    - type: precision_at_3
      value: 27.0
    - type: precision_at_5
      value: 17.8
    - type: precision_at_10
      value: 9.933
    - type: precision_at_20
      value: 5.283
    - type: precision_at_100
      value: 1.103
    - type: precision_at_1000
      value: 0.11299999999999999
    - type: mrr_at_1
      value: 62.6667
    - type: mrr_at_3
      value: 68.9444
    - type: mrr_at_5
      value: 69.9611
    - type: mrr_at_10
      value: 71.02199999999999
    - type: mrr_at_20
      value: 71.3777
    - type: mrr_at_100
      value: 71.4841
    - type: mrr_at_1000
      value: 71.4961
    - type: nauc_ndcg_at_1_max
      value: 55.4562
    - type: nauc_ndcg_at_1_std
      value: -9.3317
    - type: nauc_ndcg_at_1_diff1
      value: 71.1878
    - type: nauc_ndcg_at_3_max
      value: 55.3473
    - type: nauc_ndcg_at_3_std
      value: -14.341400000000002
    - type: nauc_ndcg_at_3_diff1
      value: 69.11880000000001
    - type: nauc_ndcg_at_5_max
      value: 55.5531
    - type: nauc_ndcg_at_5_std
      value: -13.448699999999999
    - type: nauc_ndcg_at_5_diff1
      value: 67.4611
    - type: nauc_ndcg_at_10_max
      value: 59.5974
    - type: nauc_ndcg_at_10_std
      value: -10.262
    - type: nauc_ndcg_at_10_diff1
      value: 68.3408
    - type: nauc_ndcg_at_20_max
      value: 58.586499999999994
    - type: nauc_ndcg_at_20_std
      value: -9.8438
    - type: nauc_ndcg_at_20_diff1
      value: 68.4434
    - type: nauc_ndcg_at_100_max
      value: 58.28489999999999
    - type: nauc_ndcg_at_100_std
      value: -8.7782
    - type: nauc_ndcg_at_100_diff1
      value: 68.585
    - type: nauc_ndcg_at_1000_max
      value: 58.0138
    - type: nauc_ndcg_at_1000_std
      value: -9.4827
    - type: nauc_ndcg_at_1000_diff1
      value: 69.0467
    - type: nauc_map_at_1_max
      value: 49.434
    - type: nauc_map_at_1_std
      value: -17.0503
    - type: nauc_map_at_1_diff1
      value: 71.80290000000001
    - type: nauc_map_at_3_max
      value: 52.8035
    - type: nauc_map_at_3_std
      value: -16.2138
    - type: nauc_map_at_3_diff1
      value: 69.81739999999999
    - type: nauc_map_at_5_max
      value: 54.644400000000005
    - type: nauc_map_at_5_std
      value: -13.910900000000002
    - type: nauc_map_at_5_diff1
      value: 68.8879
    - type: nauc_map_at_10_max
      value: 56.550999999999995
    - type: nauc_map_at_10_std
      value: -12.126900000000001
    - type: nauc_map_at_10_diff1
      value: 69.2326
    - type: nauc_map_at_20_max
      value: 56.299699999999994
    - type: nauc_map_at_20_std
      value: -11.8978
    - type: nauc_map_at_20_diff1
      value: 69.3387
    - type: nauc_map_at_100_max
      value: 56.295300000000005
    - type: nauc_map_at_100_std
      value: -11.6546
    - type: nauc_map_at_100_diff1
      value: 69.3881
    - type: nauc_map_at_1000_max
      value: 56.2905
    - type: nauc_map_at_1000_std
      value: -11.666400000000001
    - type: nauc_map_at_1000_diff1
      value: 69.4106
    - type: nauc_recall_at_1_max
      value: 49.434
    - type: nauc_recall_at_1_std
      value: -17.0503
    - type: nauc_recall_at_1_diff1
      value: 71.80290000000001
    - type: nauc_recall_at_3_max
      value: 53.6504
    - type: nauc_recall_at_3_std
      value: -20.3796
    - type: nauc_recall_at_3_diff1
      value: 66.0397
    - type: nauc_recall_at_5_max
      value: 54.45140000000001
    - type: nauc_recall_at_5_std
      value: -17.8965
    - type: nauc_recall_at_5_diff1
      value: 60.6996
    - type: nauc_recall_at_10_max
      value: 72.7183
    - type: nauc_recall_at_10_std
      value: -7.3393
    - type: nauc_recall_at_10_diff1
      value: 62.0422
    - type: nauc_recall_at_20_max
      value: 70.7849
    - type: nauc_recall_at_20_std
      value: -3.1933000000000002
    - type: nauc_recall_at_20_diff1
      value: 58.146
    - type: nauc_recall_at_100_max
      value: 75.43769999999999
    - type: nauc_recall_at_100_std
      value: 36.5488
    - type: nauc_recall_at_100_diff1
      value: 46.3177
    - type: nauc_recall_at_1000_max
      value: .nan
    - type: nauc_recall_at_1000_std
      value: .nan
    - type: nauc_recall_at_1000_diff1
      value: .nan
    - type: nauc_precision_at_1_max
      value: 55.4562
    - type: nauc_precision_at_1_std
      value: -9.3317
    - type: nauc_precision_at_1_diff1
      value: 71.1878
    - type: nauc_precision_at_3_max
      value: 52.548300000000005
    - type: nauc_precision_at_3_std
      value: 6.719899999999999
    - type: nauc_precision_at_3_diff1
      value: 42.6315
    - type: nauc_precision_at_5_max
      value: 47.9921
    - type: nauc_precision_at_5_std
      value: 21.9242
    - type: nauc_precision_at_5_diff1
      value: 23.0825
    - type: nauc_precision_at_10_max
      value: 47.517399999999995
    - type: nauc_precision_at_10_std
      value: 44.4913
    - type: nauc_precision_at_10_diff1
      value: 5.4589
    - type: nauc_precision_at_20_max
      value: 36.0675
    - type: nauc_precision_at_20_std
      value: 53.9269
    - type: nauc_precision_at_20_diff1
      value: -7.0865
    - type: nauc_precision_at_100_max
      value: 28.0561
    - type: nauc_precision_at_100_std
      value: 66.17920000000001
    - type: nauc_precision_at_100_diff1
      value: -19.653000000000002
    - type: nauc_precision_at_1000_max
      value: 22.470100000000002
    - type: nauc_precision_at_1000_std
      value: 69.6725
    - type: nauc_precision_at_1000_diff1
      value: -27.430500000000002
    - type: nauc_mrr_at_1_max
      value: 55.4562
    - type: nauc_mrr_at_1_std
      value: -9.3317
    - type: nauc_mrr_at_1_diff1
      value: 71.1878
    - type: nauc_mrr_at_3_max
      value: 57.4634
    - type: nauc_mrr_at_3_std
      value: -10.6496
    - type: nauc_mrr_at_3_diff1
      value: 69.881
    - type: nauc_mrr_at_5_max
      value: 56.8667
    - type: nauc_mrr_at_5_std
      value: -10.2421
    - type: nauc_mrr_at_5_diff1
      value: 69.0777
    - type: nauc_mrr_at_10_max
      value: 58.06289999999999
    - type: nauc_mrr_at_10_std
      value: -9.8724
    - type: nauc_mrr_at_10_diff1
      value: 69.5505
    - type: nauc_mrr_at_20_max
      value: 57.740700000000004
    - type: nauc_mrr_at_20_std
      value: -10.0261
    - type: nauc_mrr_at_20_diff1
      value: 69.5455
    - type: nauc_mrr_at_100_max
      value: 57.735499999999995
    - type: nauc_mrr_at_100_std
      value: -9.8413
    - type: nauc_mrr_at_100_diff1
      value: 69.5846
    - type: nauc_mrr_at_1000_max
      value: 57.7313
    - type: nauc_mrr_at_1000_std
      value: -9.8523
    - type: nauc_mrr_at_1000_diff1
      value: 69.6076
    - type: main_score
      value: 74.72
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB SprintDuplicateQuestions (default)
      revision: d66bd1f72af766a5cc4b0ca5e00c162f89e8cc46
      split: test
      type: mteb/sprintduplicatequestions-pairclassification
    metrics:
    - type: similarity_accuracy
      value: 99.798
    - type: similarity_accuracy_threshold
      value: 92.7546
    - type: similarity_f1
      value: 89.441
    - type: similarity_f1_threshold
      value: 92.7546
    - type: similarity_precision
      value: 92.70389999999999
    - type: similarity_recall
      value: 86.4
    - type: similarity_ap
      value: 95.40729999999999
    - type: cosine_accuracy
      value: 99.798
    - type: cosine_accuracy_threshold
      value: 92.7546
    - type: cosine_f1
      value: 89.441
    - type: cosine_f1_threshold
      value: 92.7546
    - type: cosine_precision
      value: 92.70389999999999
    - type: cosine_recall
      value: 86.4
    - type: cosine_ap
      value: 95.40729999999999
    - type: manhattan_accuracy
      value: 99.795
    - type: manhattan_accuracy_threshold
      value: 851.3785
    - type: manhattan_f1
      value: 89.5464
    - type: manhattan_f1_threshold
      value: 902.8005999999999
    - type: manhattan_precision
      value: 88.3268
    - type: manhattan_recall
      value: 90.8
    - type: manhattan_ap
      value: 95.3814
    - type: euclidean_accuracy
      value: 99.798
    - type: euclidean_accuracy_threshold
      value: 38.0669
    - type: euclidean_f1
      value: 89.441
    - type: euclidean_f1_threshold
      value: 38.0669
    - type: euclidean_precision
      value: 92.70389999999999
    - type: euclidean_recall
      value: 86.4
    - type: euclidean_ap
      value: 95.4074
    - type: dot_accuracy
      value: 99.798
    - type: dot_accuracy_threshold
      value: 92.7546
    - type: dot_f1
      value: 89.441
    - type: dot_f1_threshold
      value: 92.7546
    - type: dot_precision
      value: 92.70389999999999
    - type: dot_recall
      value: 86.4
    - type: dot_ap
      value: 95.4074
    - type: max_accuracy
      value: 99.798
    - type: max_f1
      value: 89.5464
    - type: max_precision
      value: 92.70389999999999
    - type: max_recall
      value: 90.8
    - type: max_ap
      value: 95.4074
    - type: main_score
      value: 95.4074
    task:
      type: PairClassification
  - dataset:
      config: default
      name: MTEB StackExchangeClustering (default)
      revision: 6cbc1f7b2bc0622f2e39d2c77fa502909748c259
      split: test
      type: mteb/stackexchange-clustering
    metrics:
    - type: v_measure
      value: 70.3156
    - type: v_measure_std
      value: 3.9677
    - type: main_score
      value: 70.3156
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB StackExchangeClusteringP2P (default)
      revision: 815ca46b2622cec33ccafc3735d572c266efdb44
      split: test
      type: mteb/stackexchange-clustering-p2p
    metrics:
    - type: v_measure
      value: 35.4198
    - type: v_measure_std
      value: 1.5537
    - type: main_score
      value: 35.4198
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB StackOverflowDupQuestions (default)
      revision: e185fbe320c72810689fc5848eb6114e1ef5ec69
      split: test
      type: mteb/stackoverflowdupquestions-reranking
    metrics:
    - type: map
      value: 54.522099999999995
    - type: mrr
      value: 55.500099999999996
    - type: nAUC_map_max
      value: 7.9342
    - type: nAUC_map_std
      value: 6.8542000000000005
    - type: nAUC_map_diff1
      value: 38.738099999999996
    - type: nAUC_mrr_max
      value: 8.862
    - type: nAUC_mrr_std
      value: 7.2187
    - type: nAUC_mrr_diff1
      value: 38.5236
    - type: main_score
      value: 54.522099999999995
    task:
      type: Reranking
  - dataset:
      config: default
      name: MTEB StackOverflowQA (default)
      revision: db8f169f3894c14a00251061f957b2063eef2bd5
      split: test
      type: CoIR-Retrieval/stackoverflow-qa
    metrics:
    - type: ndcg_at_1
      value: 83.2
    - type: ndcg_at_3
      value: 88.397
    - type: ndcg_at_5
      value: 89.202
    - type: ndcg_at_10
      value: 89.846
    - type: ndcg_at_20
      value: 90.235
    - type: ndcg_at_100
      value: 90.55199999999999
    - type: ndcg_at_1000
      value: 90.654
    - type: map_at_1
      value: 83.2
    - type: map_at_3
      value: 87.17
    - type: map_at_5
      value: 87.616
    - type: map_at_10
      value: 87.889
    - type: map_at_20
      value: 87.994
    - type: map_at_100
      value: 88.041
    - type: map_at_1000
      value: 88.045
    - type: recall_at_1
      value: 83.2
    - type: recall_at_3
      value: 91.926
    - type: recall_at_5
      value: 93.882
    - type: recall_at_10
      value: 95.838
    - type: recall_at_20
      value: 97.392
    - type: recall_at_100
      value: 99.047
    - type: recall_at_1000
      value: 99.85000000000001
    - type: precision_at_1
      value: 83.2
    - type: precision_at_3
      value: 30.642000000000003
    - type: precision_at_5
      value: 18.776
    - type: precision_at_10
      value: 9.584
    - type: precision_at_20
      value: 4.87
    - type: precision_at_100
      value: 0.9900000000000001
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 83.19959999999999
    - type: mrr_at_3
      value: 87.1698
    - type: mrr_at_5
      value: 87.6162
    - type: mrr_at_10
      value: 87.8891
    - type: mrr_at_20
      value: 87.99369999999999
    - type: mrr_at_100
      value: 88.0412
    - type: mrr_at_1000
      value: 88.045
    - type: nauc_ndcg_at_1_max
      value: 78.6007
    - type: nauc_ndcg_at_1_std
      value: -0.0095
    - type: nauc_ndcg_at_1_diff1
      value: 88.7762
    - type: nauc_ndcg_at_3_max
      value: 81.4239
    - type: nauc_ndcg_at_3_std
      value: 1.4683
    - type: nauc_ndcg_at_3_diff1
      value: 86.54220000000001
    - type: nauc_ndcg_at_5_max
      value: 80.8469
    - type: nauc_ndcg_at_5_std
      value: -0.5089
    - type: nauc_ndcg_at_5_diff1
      value: 86.7397
    - type: nauc_ndcg_at_10_max
      value: 80.60730000000001
    - type: nauc_ndcg_at_10_std
      value: 1.2302
    - type: nauc_ndcg_at_10_diff1
      value: 86.5722
    - type: nauc_ndcg_at_20_max
      value: 80.5133
    - type: nauc_ndcg_at_20_std
      value: 1.0021
    - type: nauc_ndcg_at_20_diff1
      value: 86.6381
    - type: nauc_ndcg_at_100_max
      value: 80.4389
    - type: nauc_ndcg_at_100_std
      value: 0.33
    - type: nauc_ndcg_at_100_diff1
      value: 86.993
    - type: nauc_ndcg_at_1000_max
      value: 80.3736
    - type: nauc_ndcg_at_1000_std
      value: 0.582
    - type: nauc_ndcg_at_1000_diff1
      value: 86.9238
    - type: nauc_map_at_1_max
      value: 78.6007
    - type: nauc_map_at_1_std
      value: -0.0095
    - type: nauc_map_at_1_diff1
      value: 88.7762
    - type: nauc_map_at_3_max
      value: 80.6167
    - type: nauc_map_at_3_std
      value: 0.8933
    - type: nauc_map_at_3_diff1
      value: 87.07629999999999
    - type: nauc_map_at_5_max
      value: 80.3056
    - type: nauc_map_at_5_std
      value: -0.1035
    - type: nauc_map_at_5_diff1
      value: 87.1974
    - type: nauc_map_at_10_max
      value: 80.1979
    - type: nauc_map_at_10_std
      value: 0.4875
    - type: nauc_map_at_10_diff1
      value: 87.1597
    - type: nauc_map_at_20_max
      value: 80.1758
    - type: nauc_map_at_20_std
      value: 0.4484
    - type: nauc_map_at_20_diff1
      value: 87.1785
    - type: nauc_map_at_100_max
      value: 80.1598
    - type: nauc_map_at_100_std
      value: 0.3517
    - type: nauc_map_at_100_diff1
      value: 87.2128
    - type: nauc_map_at_1000_max
      value: 80.1585
    - type: nauc_map_at_1000_std
      value: 0.3646
    - type: nauc_map_at_1000_diff1
      value: 87.2108
    - type: nauc_recall_at_1_max
      value: 78.6007
    - type: nauc_recall_at_1_std
      value: -0.0095
    - type: nauc_recall_at_1_diff1
      value: 88.7762
    - type: nauc_recall_at_3_max
      value: 84.951
    - type: nauc_recall_at_3_std
      value: 4.0854
    - type: nauc_recall_at_3_diff1
      value: 84.2801
    - type: nauc_recall_at_5_max
      value: 83.68339999999999
    - type: nauc_recall_at_5_std
      value: -3.1815
    - type: nauc_recall_at_5_diff1
      value: 84.33619999999999
    - type: nauc_recall_at_10_max
      value: 83.4402
    - type: nauc_recall_at_10_std
      value: 8.585700000000001
    - type: nauc_recall_at_10_diff1
      value: 81.84320000000001
    - type: nauc_recall_at_20_max
      value: 83.6935
    - type: nauc_recall_at_20_std
      value: 9.088799999999999
    - type: nauc_recall_at_20_diff1
      value: 80.01
    - type: nauc_recall_at_100_max
      value: 86.5116
    - type: nauc_recall_at_100_std
      value: -7.6839
    - type: nauc_recall_at_100_diff1
      value: 88.1354
    - type: nauc_recall_at_1000_max
      value: 86.3848
    - type: nauc_recall_at_1000_std
      value: 52.8467
    - type: nauc_recall_at_1000_diff1
      value: 61.4995
    - type: nauc_precision_at_1_max
      value: 78.6007
    - type: nauc_precision_at_1_std
      value: -0.0095
    - type: nauc_precision_at_1_diff1
      value: 88.7762
    - type: nauc_precision_at_3_max
      value: 84.951
    - type: nauc_precision_at_3_std
      value: 4.0854
    - type: nauc_precision_at_3_diff1
      value: 84.2801
    - type: nauc_precision_at_5_max
      value: 83.68339999999999
    - type: nauc_precision_at_5_std
      value: -3.1815
    - type: nauc_precision_at_5_diff1
      value: 84.33619999999999
    - type: nauc_precision_at_10_max
      value: 83.4402
    - type: nauc_precision_at_10_std
      value: 8.585700000000001
    - type: nauc_precision_at_10_diff1
      value: 81.84320000000001
    - type: nauc_precision_at_20_max
      value: 83.6935
    - type: nauc_precision_at_20_std
      value: 9.088799999999999
    - type: nauc_precision_at_20_diff1
      value: 80.01
    - type: nauc_precision_at_100_max
      value: 86.5116
    - type: nauc_precision_at_100_std
      value: -7.6839
    - type: nauc_precision_at_100_diff1
      value: 88.1354
    - type: nauc_precision_at_1000_max
      value: 86.3848
    - type: nauc_precision_at_1000_std
      value: 52.8467
    - type: nauc_precision_at_1000_diff1
      value: 61.4995
    - type: nauc_mrr_at_1_max
      value: 78.6007
    - type: nauc_mrr_at_1_std
      value: -0.0095
    - type: nauc_mrr_at_1_diff1
      value: 88.7762
    - type: nauc_mrr_at_3_max
      value: 80.6167
    - type: nauc_mrr_at_3_std
      value: 0.8933
    - type: nauc_mrr_at_3_diff1
      value: 87.07629999999999
    - type: nauc_mrr_at_5_max
      value: 80.3056
    - type: nauc_mrr_at_5_std
      value: -0.1035
    - type: nauc_mrr_at_5_diff1
      value: 87.1974
    - type: nauc_mrr_at_10_max
      value: 80.1979
    - type: nauc_mrr_at_10_std
      value: 0.4875
    - type: nauc_mrr_at_10_diff1
      value: 87.1597
    - type: nauc_mrr_at_20_max
      value: 80.1758
    - type: nauc_mrr_at_20_std
      value: 0.4484
    - type: nauc_mrr_at_20_diff1
      value: 87.1785
    - type: nauc_mrr_at_100_max
      value: 80.1598
    - type: nauc_mrr_at_100_std
      value: 0.3517
    - type: nauc_mrr_at_100_diff1
      value: 87.2128
    - type: nauc_mrr_at_1000_max
      value: 80.1585
    - type: nauc_mrr_at_1000_std
      value: 0.3646
    - type: nauc_mrr_at_1000_diff1
      value: 87.2108
    - type: main_score
      value: 89.846
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB SummEval (default)
      revision: cda12ad7615edc362dbf25a00fdd61d3b1eaf93c
      split: test
      type: mteb/summeval
    metrics:
    - type: pearson
      value: 30.709999999999997
    - type: spearman
      value: 31.841199999999997
    - type: cosine_spearman
      value: 31.841199999999997
    - type: cosine_pearson
      value: 30.709999999999997
    - type: dot_spearman
      value: 31.841199999999997
    - type: dot_pearson
      value: 30.709999999999997
    - type: main_score
      value: 31.841199999999997
    task:
      type: Summarization
  - dataset:
      config: default
      name: MTEB SyntheticText2SQL (default)
      revision: 686b87296c3a0191b5d9415a00526c62db9fce09
      split: test
      type: CoIR-Retrieval/synthetic-text2sql
    metrics:
    - type: ndcg_at_1
      value: 3.692
    - type: ndcg_at_3
      value: 42.481
    - type: ndcg_at_5
      value: 45.909
    - type: ndcg_at_10
      value: 48.41
    - type: ndcg_at_20
      value: 49.845
    - type: ndcg_at_100
      value: 51.358000000000004
    - type: ndcg_at_1000
      value: 51.739999999999995
    - type: map_at_1
      value: 3.692
    - type: map_at_3
      value: 33.82
    - type: map_at_5
      value: 35.727
    - type: map_at_10
      value: 36.768
    - type: map_at_20
      value: 37.162
    - type: map_at_100
      value: 37.377
    - type: map_at_1000
      value: 37.391999999999996
    - type: recall_at_1
      value: 3.692
    - type: recall_at_3
      value: 67.18499999999999
    - type: recall_at_5
      value: 75.491
    - type: recall_at_10
      value: 83.182
    - type: recall_at_20
      value: 88.857
    - type: recall_at_100
      value: 96.92399999999999
    - type: recall_at_1000
      value: 99.88
    - type: precision_at_1
      value: 3.692
    - type: precision_at_3
      value: 22.395
    - type: precision_at_5
      value: 15.098
    - type: precision_at_10
      value: 8.318
    - type: precision_at_20
      value: 4.443
    - type: precision_at_100
      value: 0.9690000000000001
    - type: precision_at_1000
      value: 0.1
    - type: mrr_at_1
      value: 31.4647
    - type: mrr_at_3
      value: 49.3391
    - type: mrr_at_5
      value: 50.9842
    - type: mrr_at_10
      value: 51.902499999999996
    - type: mrr_at_20
      value: 52.2801
    - type: mrr_at_100
      value: 52.4906
    - type: mrr_at_1000
      value: 52.506
    - type: nauc_ndcg_at_1_max
      value: 5.9474
    - type: nauc_ndcg_at_1_std
      value: -15.6036
    - type: nauc_ndcg_at_1_diff1
      value: 74.4115
    - type: nauc_ndcg_at_3_max
      value: 24.1744
    - type: nauc_ndcg_at_3_std
      value: -26.2412
    - type: nauc_ndcg_at_3_diff1
      value: -61.795
    - type: nauc_ndcg_at_5_max
      value: 24.3445
    - type: nauc_ndcg_at_5_std
      value: -26.8005
    - type: nauc_ndcg_at_5_diff1
      value: -57.8936
    - type: nauc_ndcg_at_10_max
      value: 23.6218
    - type: nauc_ndcg_at_10_std
      value: -26.378400000000003
    - type: nauc_ndcg_at_10_diff1
      value: -54.496599999999994
    - type: nauc_ndcg_at_20_max
      value: 23.6458
    - type: nauc_ndcg_at_20_std
      value: -26.1137
    - type: nauc_ndcg_at_20_diff1
      value: -52.7814
    - type: nauc_ndcg_at_100_max
      value: 23.59
    - type: nauc_ndcg_at_100_std
      value: -24.786
    - type: nauc_ndcg_at_100_diff1
      value: -51.30200000000001
    - type: nauc_ndcg_at_1000_max
      value: 23.1129
    - type: nauc_ndcg_at_1000_std
      value: -25.138899999999996
    - type: nauc_ndcg_at_1000_diff1
      value: -50.856500000000004
    - type: nauc_map_at_1_max
      value: 5.9474
    - type: nauc_map_at_1_std
      value: -15.6036
    - type: nauc_map_at_1_diff1
      value: 74.4115
    - type: nauc_map_at_3_max
      value: 22.7683
    - type: nauc_map_at_3_std
      value: -25.060399999999998
    - type: nauc_map_at_3_diff1
      value: -53.0054
    - type: nauc_map_at_5_max
      value: 22.778100000000002
    - type: nauc_map_at_5_std
      value: -25.3076
    - type: nauc_map_at_5_diff1
      value: -49.921
    - type: nauc_map_at_10_max
      value: 22.345000000000002
    - type: nauc_map_at_10_std
      value: -25.0615
    - type: nauc_map_at_10_diff1
      value: -48.089999999999996
    - type: nauc_map_at_20_max
      value: 22.336100000000002
    - type: nauc_map_at_20_std
      value: -24.9463
    - type: nauc_map_at_20_diff1
      value: -47.4815
    - type: nauc_map_at_100_max
      value: 22.3039
    - type: nauc_map_at_100_std
      value: -24.7562
    - type: nauc_map_at_100_diff1
      value: -47.2248
    - type: nauc_map_at_1000_max
      value: 22.287000000000003
    - type: nauc_map_at_1000_std
      value: -24.7638
    - type: nauc_map_at_1000_diff1
      value: -47.2029
    - type: nauc_recall_at_1_max
      value: 5.9474
    - type: nauc_recall_at_1_std
      value: -15.6036
    - type: nauc_recall_at_1_diff1
      value: 74.4115
    - type: nauc_recall_at_3_max
      value: 26.7488
    - type: nauc_recall_at_3_std
      value: -28.5119
    - type: nauc_recall_at_3_diff1
      value: -77.3694
    - type: nauc_recall_at_5_max
      value: 27.694499999999998
    - type: nauc_recall_at_5_std
      value: -30.2099
    - type: nauc_recall_at_5_diff1
      value: -73.6265
    - type: nauc_recall_at_10_max
      value: 26.9417
    - type: nauc_recall_at_10_std
      value: -30.1319
    - type: nauc_recall_at_10_diff1
      value: -68.8477
    - type: nauc_recall_at_20_max
      value: 28.432800000000004
    - type: nauc_recall_at_20_std
      value: -30.55
    - type: nauc_recall_at_20_diff1
      value: -66.2201
    - type: nauc_recall_at_100_max
      value: 39.7358
    - type: nauc_recall_at_100_std
      value: -11.5261
    - type: nauc_recall_at_100_diff1
      value: -66.6477
    - type: nauc_recall_at_1000_max
      value: 34.353
    - type: nauc_recall_at_1000_std
      value: -6.297899999999999
    - type: nauc_recall_at_1000_diff1
      value: -85.7774
    - type: nauc_precision_at_1_max
      value: 5.9474
    - type: nauc_precision_at_1_std
      value: -15.6036
    - type: nauc_precision_at_1_diff1
      value: 74.4115
    - type: nauc_precision_at_3_max
      value: 26.7488
    - type: nauc_precision_at_3_std
      value: -28.5119
    - type: nauc_precision_at_3_diff1
      value: -77.3694
    - type: nauc_precision_at_5_max
      value: 27.694499999999998
    - type: nauc_precision_at_5_std
      value: -30.2099
    - type: nauc_precision_at_5_diff1
      value: -73.6265
    - type: nauc_precision_at_10_max
      value: 26.9417
    - type: nauc_precision_at_10_std
      value: -30.1319
    - type: nauc_precision_at_10_diff1
      value: -68.8477
    - type: nauc_precision_at_20_max
      value: 28.432800000000004
    - type: nauc_precision_at_20_std
      value: -30.55
    - type: nauc_precision_at_20_diff1
      value: -66.2201
    - type: nauc_precision_at_100_max
      value: 39.7358
    - type: nauc_precision_at_100_std
      value: -11.5261
    - type: nauc_precision_at_100_diff1
      value: -66.6477
    - type: nauc_precision_at_1000_max
      value: 34.353
    - type: nauc_precision_at_1000_std
      value: -6.297899999999999
    - type: nauc_precision_at_1000_diff1
      value: -85.7774
    - type: nauc_mrr_at_1_max
      value: 14.005899999999999
    - type: nauc_mrr_at_1_std
      value: -13.7382
    - type: nauc_mrr_at_1_diff1
      value: -36.567499999999995
    - type: nauc_mrr_at_3_max
      value: 19.6693
    - type: nauc_mrr_at_3_std
      value: -19.7679
    - type: nauc_mrr_at_3_diff1
      value: -54.849000000000004
    - type: nauc_mrr_at_5_max
      value: 19.4039
    - type: nauc_mrr_at_5_std
      value: -19.822
    - type: nauc_mrr_at_5_diff1
      value: -53.7619
    - type: nauc_mrr_at_10_max
      value: 19.1888
    - type: nauc_mrr_at_10_std
      value: -19.4663
    - type: nauc_mrr_at_10_diff1
      value: -52.9212
    - type: nauc_mrr_at_20_max
      value: 19.1218
    - type: nauc_mrr_at_20_std
      value: -19.378600000000002
    - type: nauc_mrr_at_20_diff1
      value: -52.663000000000004
    - type: nauc_mrr_at_100_max
      value: 19.089100000000002
    - type: nauc_mrr_at_100_std
      value: -19.2391
    - type: nauc_mrr_at_100_diff1
      value: -52.5536
    - type: nauc_mrr_at_1000_max
      value: 19.078400000000002
    - type: nauc_mrr_at_1000_std
      value: -19.240099999999998
    - type: nauc_mrr_at_1000_diff1
      value: -52.544900000000005
    - type: main_score
      value: 48.41
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB TRECCOVID (default)
      revision: bb9466bac8153a0349341eb1b22e06409e78ef4e
      split: test
      type: mteb/trec-covid
    metrics:
    - type: ndcg_at_1
      value: 66.0
    - type: ndcg_at_3
      value: 70.654
    - type: ndcg_at_5
      value: 71.611
    - type: ndcg_at_10
      value: 69.259
    - type: ndcg_at_20
      value: 67.02
    - type: ndcg_at_100
      value: 57.274
    - type: ndcg_at_1000
      value: 55.459
    - type: map_at_1
      value: 0.202
    - type: map_at_3
      value: 0.553
    - type: map_at_5
      value: 0.924
    - type: map_at_10
      value: 1.727
    - type: map_at_20
      value: 3.124
    - type: map_at_100
      value: 10.906
    - type: map_at_1000
      value: 28.938999999999997
    - type: recall_at_1
      value: 0.202
    - type: recall_at_3
      value: 0.609
    - type: recall_at_5
      value: 1.048
    - type: recall_at_10
      value: 2.001
    - type: recall_at_20
      value: 3.749
    - type: recall_at_100
      value: 14.801
    - type: recall_at_1000
      value: 53.93599999999999
    - type: precision_at_1
      value: 74.0
    - type: precision_at_3
      value: 77.333
    - type: precision_at_5
      value: 78.8
    - type: precision_at_10
      value: 74.8
    - type: precision_at_20
      value: 72.0
    - type: precision_at_100
      value: 59.62
    - type: precision_at_1000
      value: 24.84
    - type: mrr_at_1
      value: 74.0
    - type: mrr_at_3
      value: 85.66669999999999
    - type: mrr_at_5
      value: 85.66669999999999
    - type: mrr_at_10
      value: 85.66669999999999
    - type: mrr_at_20
      value: 85.66669999999999
    - type: mrr_at_100
      value: 85.66669999999999
    - type: mrr_at_1000
      value: 85.66669999999999
    - type: nauc_ndcg_at_1_max
      value: 36.0347
    - type: nauc_ndcg_at_1_std
      value: 41.708099999999995
    - type: nauc_ndcg_at_1_diff1
      value: 13.226099999999999
    - type: nauc_ndcg_at_3_max
      value: 45.4255
    - type: nauc_ndcg_at_3_std
      value: 49.8257
    - type: nauc_ndcg_at_3_diff1
      value: -0.44520000000000004
    - type: nauc_ndcg_at_5_max
      value: 49.6908
    - type: nauc_ndcg_at_5_std
      value: 54.221
    - type: nauc_ndcg_at_5_diff1
      value: 3.5483000000000002
    - type: nauc_ndcg_at_10_max
      value: 46.2419
    - type: nauc_ndcg_at_10_std
      value: 59.9826
    - type: nauc_ndcg_at_10_diff1
      value: -0.436
    - type: nauc_ndcg_at_20_max
      value: 42.3528
    - type: nauc_ndcg_at_20_std
      value: 64.9208
    - type: nauc_ndcg_at_20_diff1
      value: -15.72
    - type: nauc_ndcg_at_100_max
      value: 38.6688
    - type: nauc_ndcg_at_100_std
      value: 70.27069999999999
    - type: nauc_ndcg_at_100_diff1
      value: -27.691900000000004
    - type: nauc_ndcg_at_1000_max
      value: 39.3229
    - type: nauc_ndcg_at_1000_std
      value: 71.5958
    - type: nauc_ndcg_at_1000_diff1
      value: -32.426899999999996
    - type: nauc_map_at_1_max
      value: 24.9717
    - type: nauc_map_at_1_std
      value: 20.3237
    - type: nauc_map_at_1_diff1
      value: 26.8022
    - type: nauc_map_at_3_max
      value: 36.496
    - type: nauc_map_at_3_std
      value: 32.506
    - type: nauc_map_at_3_diff1
      value: 17.7469
    - type: nauc_map_at_5_max
      value: 37.802
    - type: nauc_map_at_5_std
      value: 32.5133
    - type: nauc_map_at_5_diff1
      value: 21.9404
    - type: nauc_map_at_10_max
      value: 36.8446
    - type: nauc_map_at_10_std
      value: 37.3347
    - type: nauc_map_at_10_diff1
      value: 23.311
    - type: nauc_map_at_20_max
      value: 35.484500000000004
    - type: nauc_map_at_20_std
      value: 42.1774
    - type: nauc_map_at_20_diff1
      value: 14.072499999999998
    - type: nauc_map_at_100_max
      value: 38.3755
    - type: nauc_map_at_100_std
      value: 58.458299999999994
    - type: nauc_map_at_100_diff1
      value: -7.320200000000001
    - type: nauc_map_at_1000_max
      value: 43.0209
    - type: nauc_map_at_1000_std
      value: 72.8673
    - type: nauc_map_at_1000_diff1
      value: -29.952299999999997
    - type: nauc_recall_at_1_max
      value: 24.9717
    - type: nauc_recall_at_1_std
      value: 20.3237
    - type: nauc_recall_at_1_diff1
      value: 26.8022
    - type: nauc_recall_at_3_max
      value: 29.149900000000002
    - type: nauc_recall_at_3_std
      value: 27.2806
    - type: nauc_recall_at_3_diff1
      value: 16.0975
    - type: nauc_recall_at_5_max
      value: 29.3013
    - type: nauc_recall_at_5_std
      value: 26.4035
    - type: nauc_recall_at_5_diff1
      value: 20.3157
    - type: nauc_recall_at_10_max
      value: 27.326099999999997
    - type: nauc_recall_at_10_std
      value: 30.1061
    - type: nauc_recall_at_10_diff1
      value: 22.0122
    - type: nauc_recall_at_20_max
      value: 25.176399999999997
    - type: nauc_recall_at_20_std
      value: 33.1536
    - type: nauc_recall_at_20_diff1
      value: 13.4285
    - type: nauc_recall_at_100_max
      value: 28.209899999999998
    - type: nauc_recall_at_100_std
      value: 45.7222
    - type: nauc_recall_at_100_diff1
      value: -6.1627
    - type: nauc_recall_at_1000_max
      value: 33.4423
    - type: nauc_recall_at_1000_std
      value: 60.764399999999995
    - type: nauc_recall_at_1000_diff1
      value: -32.4319
    - type: nauc_precision_at_1_max
      value: 55.0789
    - type: nauc_precision_at_1_std
      value: 42.7355
    - type: nauc_precision_at_1_diff1
      value: 21.276500000000002
    - type: nauc_precision_at_3_max
      value: 57.5971
    - type: nauc_precision_at_3_std
      value: 54.4791
    - type: nauc_precision_at_3_diff1
      value: -1.1622000000000001
    - type: nauc_precision_at_5_max
      value: 66.64750000000001
    - type: nauc_precision_at_5_std
      value: 57.5585
    - type: nauc_precision_at_5_diff1
      value: 2.9311
    - type: nauc_precision_at_10_max
      value: 58.767100000000006
    - type: nauc_precision_at_10_std
      value: 63.5528
    - type: nauc_precision_at_10_diff1
      value: -1.193
    - type: nauc_precision_at_20_max
      value: 47.964
    - type: nauc_precision_at_20_std
      value: 65.3738
    - type: nauc_precision_at_20_diff1
      value: -17.0707
    - type: nauc_precision_at_100_max
      value: 38.9039
    - type: nauc_precision_at_100_std
      value: 68.9848
    - type: nauc_precision_at_100_diff1
      value: -31.816699999999997
    - type: nauc_precision_at_1000_max
      value: 24.090700000000002
    - type: nauc_precision_at_1000_std
      value: 36.3251
    - type: nauc_precision_at_1000_diff1
      value: -30.1565
    - type: nauc_mrr_at_1_max
      value: 55.0789
    - type: nauc_mrr_at_1_std
      value: 42.7355
    - type: nauc_mrr_at_1_diff1
      value: 21.276500000000002
    - type: nauc_mrr_at_3_max
      value: 57.0157
    - type: nauc_mrr_at_3_std
      value: 44.9613
    - type: nauc_mrr_at_3_diff1
      value: 18.5485
    - type: nauc_mrr_at_5_max
      value: 57.0157
    - type: nauc_mrr_at_5_std
      value: 44.9613
    - type: nauc_mrr_at_5_diff1
      value: 18.5485
    - type: nauc_mrr_at_10_max
      value: 57.0157
    - type: nauc_mrr_at_10_std
      value: 44.9613
    - type: nauc_mrr_at_10_diff1
      value: 18.5485
    - type: nauc_mrr_at_20_max
      value: 57.0157
    - type: nauc_mrr_at_20_std
      value: 44.9613
    - type: nauc_mrr_at_20_diff1
      value: 18.5485
    - type: nauc_mrr_at_100_max
      value: 57.0157
    - type: nauc_mrr_at_100_std
      value: 44.9613
    - type: nauc_mrr_at_100_diff1
      value: 18.5485
    - type: nauc_mrr_at_1000_max
      value: 57.0157
    - type: nauc_mrr_at_1000_std
      value: 44.9613
    - type: nauc_mrr_at_1000_diff1
      value: 18.5485
    - type: main_score
      value: 69.259
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB Touche2020 (default)
      revision: a34f9a33db75fa0cbb21bb5cfc3dae8dc8bec93f
      split: test
      type: mteb/touche2020
    metrics:
    - type: ndcg_at_1
      value: 23.469
    - type: ndcg_at_3
      value: 22.555
    - type: ndcg_at_5
      value: 20.97
    - type: ndcg_at_10
      value: 20.147000000000002
    - type: ndcg_at_20
      value: 22.56
    - type: ndcg_at_100
      value: 32.79
    - type: ndcg_at_1000
      value: 45.324
    - type: map_at_1
      value: 2.152
    - type: map_at_3
      value: 4.103
    - type: map_at_5
      value: 5.482
    - type: map_at_10
      value: 7.747
    - type: map_at_20
      value: 10.309
    - type: map_at_100
      value: 13.639999999999999
    - type: map_at_1000
      value: 15.235000000000001
    - type: recall_at_1
      value: 2.152
    - type: recall_at_3
      value: 5.531
    - type: recall_at_5
      value: 8.029
    - type: recall_at_10
      value: 13.331000000000001
    - type: recall_at_20
      value: 22.195
    - type: recall_at_100
      value: 45.35
    - type: recall_at_1000
      value: 83.447
    - type: precision_at_1
      value: 26.531
    - type: precision_at_3
      value: 24.490000000000002
    - type: precision_at_5
      value: 21.633
    - type: precision_at_10
      value: 17.755000000000003
    - type: precision_at_20
      value: 15.408
    - type: precision_at_100
      value: 7.081999999999999
    - type: precision_at_1000
      value: 1.547
    - type: mrr_at_1
      value: 26.5306
    - type: mrr_at_3
      value: 38.7755
    - type: mrr_at_5
      value: 40.6122
    - type: mrr_at_10
      value: 41.3994
    - type: mrr_at_20
      value: 42.7601
    - type: mrr_at_100
      value: 43.0467
    - type: mrr_at_1000
      value: 43.0467
    - type: nauc_ndcg_at_1_max
      value: -19.1831
    - type: nauc_ndcg_at_1_std
      value: -13.1044
    - type: nauc_ndcg_at_1_diff1
      value: -8.6701
    - type: nauc_ndcg_at_3_max
      value: -31.2521
    - type: nauc_ndcg_at_3_std
      value: -9.1974
    - type: nauc_ndcg_at_3_diff1
      value: -17.0766
    - type: nauc_ndcg_at_5_max
      value: -29.9171
    - type: nauc_ndcg_at_5_std
      value: -2.2094
    - type: nauc_ndcg_at_5_diff1
      value: -10.8668
    - type: nauc_ndcg_at_10_max
      value: -24.5148
    - type: nauc_ndcg_at_10_std
      value: -0.45909999999999995
    - type: nauc_ndcg_at_10_diff1
      value: -10.705
    - type: nauc_ndcg_at_20_max
      value: -29.542
    - type: nauc_ndcg_at_20_std
      value: -0.1119
    - type: nauc_ndcg_at_20_diff1
      value: -6.4151
    - type: nauc_ndcg_at_100_max
      value: -27.276
    - type: nauc_ndcg_at_100_std
      value: 33.380900000000004
    - type: nauc_ndcg_at_100_diff1
      value: -1.097
    - type: nauc_ndcg_at_1000_max
      value: -28.0856
    - type: nauc_ndcg_at_1000_std
      value: 40.368700000000004
    - type: nauc_ndcg_at_1000_diff1
      value: -9.5892
    - type: nauc_map_at_1_max
      value: -17.891099999999998
    - type: nauc_map_at_1_std
      value: -20.8139
    - type: nauc_map_at_1_diff1
      value: 2.1289
    - type: nauc_map_at_3_max
      value: -18.5984
    - type: nauc_map_at_3_std
      value: -16.0226
    - type: nauc_map_at_3_diff1
      value: -0.681
    - type: nauc_map_at_5_max
      value: -9.8672
    - type: nauc_map_at_5_std
      value: -11.448
    - type: nauc_map_at_5_diff1
      value: 4.1101
    - type: nauc_map_at_10_max
      value: -5.8905
    - type: nauc_map_at_10_std
      value: -7.7416
    - type: nauc_map_at_10_diff1
      value: 2.0848999999999998
    - type: nauc_map_at_20_max
      value: -13.9206
    - type: nauc_map_at_20_std
      value: -4.9227
    - type: nauc_map_at_20_diff1
      value: 1.6968
    - type: nauc_map_at_100_max
      value: -15.116
    - type: nauc_map_at_100_std
      value: 10.9804
    - type: nauc_map_at_100_diff1
      value: 1.5921999999999998
    - type: nauc_map_at_1000_max
      value: -15.309000000000001
    - type: nauc_map_at_1000_std
      value: 15.207399999999998
    - type: nauc_map_at_1000_diff1
      value: 0.2635
    - type: nauc_recall_at_1_max
      value: -17.891099999999998
    - type: nauc_recall_at_1_std
      value: -20.8139
    - type: nauc_recall_at_1_diff1
      value: 2.1289
    - type: nauc_recall_at_3_max
      value: -27.4434
    - type: nauc_recall_at_3_std
      value: -14.4615
    - type: nauc_recall_at_3_diff1
      value: -4.6056
    - type: nauc_recall_at_5_max
      value: -17.3993
    - type: nauc_recall_at_5_std
      value: -7.1856
    - type: nauc_recall_at_5_diff1
      value: 2.468
    - type: nauc_recall_at_10_max
      value: -13.7175
    - type: nauc_recall_at_10_std
      value: -2.9436
    - type: nauc_recall_at_10_diff1
      value: 0.9384
    - type: nauc_recall_at_20_max
      value: -26.96
    - type: nauc_recall_at_20_std
      value: -1.6922
    - type: nauc_recall_at_20_diff1
      value: 1.8932999999999998
    - type: nauc_recall_at_100_max
      value: -23.5556
    - type: nauc_recall_at_100_std
      value: 48.9062
    - type: nauc_recall_at_100_diff1
      value: 7.8596
    - type: nauc_recall_at_1000_max
      value: -19.6066
    - type: nauc_recall_at_1000_std
      value: 80.4306
    - type: nauc_recall_at_1000_diff1
      value: -8.4789
    - type: nauc_precision_at_1_max
      value: -23.163800000000002
    - type: nauc_precision_at_1_std
      value: -15.9221
    - type: nauc_precision_at_1_diff1
      value: -1.0075
    - type: nauc_precision_at_3_max
      value: -34.2
    - type: nauc_precision_at_3_std
      value: -5.8114
    - type: nauc_precision_at_3_diff1
      value: -11.4192
    - type: nauc_precision_at_5_max
      value: -28.3543
    - type: nauc_precision_at_5_std
      value: 3.2409
    - type: nauc_precision_at_5_diff1
      value: -2.4743
    - type: nauc_precision_at_10_max
      value: -21.8691
    - type: nauc_precision_at_10_std
      value: 12.0827
    - type: nauc_precision_at_10_diff1
      value: -7.6671000000000005
    - type: nauc_precision_at_20_max
      value: -29.541600000000003
    - type: nauc_precision_at_20_std
      value: 18.4544
    - type: nauc_precision_at_20_diff1
      value: -4.9384
    - type: nauc_precision_at_100_max
      value: -13.991700000000002
    - type: nauc_precision_at_100_std
      value: 80.9784
    - type: nauc_precision_at_100_diff1
      value: 0.1001
    - type: nauc_precision_at_1000_max
      value: 18.334
    - type: nauc_precision_at_1000_std
      value: 35.3463
    - type: nauc_precision_at_1000_diff1
      value: -16.8628
    - type: nauc_mrr_at_1_max
      value: -23.163800000000002
    - type: nauc_mrr_at_1_std
      value: -15.9221
    - type: nauc_mrr_at_1_diff1
      value: -1.0075
    - type: nauc_mrr_at_3_max
      value: -37.628099999999996
    - type: nauc_mrr_at_3_std
      value: -13.678199999999999
    - type: nauc_mrr_at_3_diff1
      value: -8.0387
    - type: nauc_mrr_at_5_max
      value: -38.205
    - type: nauc_mrr_at_5_std
      value: -10.0574
    - type: nauc_mrr_at_5_diff1
      value: -7.273300000000001
    - type: nauc_mrr_at_10_max
      value: -38.2773
    - type: nauc_mrr_at_10_std
      value: -10.5208
    - type: nauc_mrr_at_10_diff1
      value: -7.556400000000001
    - type: nauc_mrr_at_20_max
      value: -38.8068
    - type: nauc_mrr_at_20_std
      value: -10.7195
    - type: nauc_mrr_at_20_diff1
      value: -6.7631
    - type: nauc_mrr_at_100_max
      value: -38.318200000000004
    - type: nauc_mrr_at_100_std
      value: -10.854999999999999
    - type: nauc_mrr_at_100_diff1
      value: -6.843000000000001
    - type: nauc_mrr_at_1000_max
      value: -38.318200000000004
    - type: nauc_mrr_at_1000_std
      value: -10.854999999999999
    - type: nauc_mrr_at_1000_diff1
      value: -6.843000000000001
    - type: main_score
      value: 20.147000000000002
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB ToxicConversationsClassification (default)
      revision: edfaf9da55d3dd50d43143d90c1ac476895ae6de
      split: test
      type: mteb/toxic_conversations_50k
    metrics:
    - type: accuracy
      value: 59.7607
    - type: f1
      value: 45.7266
    - type: f1_weighted
      value: 68.3382
    - type: ap
      value: 9.8682
    - type: ap_weighted
      value: 9.8682
    - type: main_score
      value: 59.7607
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB TweetSentimentExtractionClassification (default)
      revision: d604517c81ca91fe16a244d1248fc021f9ecee7a
      split: test
      type: mteb/tweet_sentiment_extraction
    metrics:
    - type: accuracy
      value: 53.3192
    - type: f1
      value: 53.505100000000006
    - type: f1_weighted
      value: 52.726600000000005
    - type: main_score
      value: 53.3192
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB TwentyNewsgroupsClustering (default)
      revision: 6125ec4e24fa026cec8a478383ee943acfbd5449
      split: test
      type: mteb/twentynewsgroups-clustering
    metrics:
    - type: v_measure
      value: 48.3133
    - type: v_measure_std
      value: 1.6674000000000002
    - type: main_score
      value: 48.3133
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB TwitterSemEval2015 (default)
      revision: 70970daeab8776df92f5ea462b6173c0b46fd2d1
      split: test
      type: mteb/twittersemeval2015-pairclassification
    metrics:
    - type: similarity_accuracy
      value: 82.2972
    - type: similarity_accuracy_threshold
      value: 92.5986
    - type: similarity_f1
      value: 58.2994
    - type: similarity_f1_threshold
      value: 89.689
    - type: similarity_precision
      value: 53.3772
    - type: similarity_recall
      value: 64.2216
    - type: similarity_ap
      value: 60.9374
    - type: cosine_accuracy
      value: 82.2972
    - type: cosine_accuracy_threshold
      value: 92.5986
    - type: cosine_f1
      value: 58.2994
    - type: cosine_f1_threshold
      value: 89.689
    - type: cosine_precision
      value: 53.3772
    - type: cosine_recall
      value: 64.2216
    - type: cosine_ap
      value: 60.9374
    - type: manhattan_accuracy
      value: 82.2912
    - type: manhattan_accuracy_threshold
      value: 839.1809000000001
    - type: manhattan_f1
      value: 58.2447
    - type: manhattan_f1_threshold
      value: 996.9049
    - type: manhattan_precision
      value: 53.74830000000001
    - type: manhattan_recall
      value: 63.562
    - type: manhattan_ap
      value: 60.8808
    - type: euclidean_accuracy
      value: 82.2972
    - type: euclidean_accuracy_threshold
      value: 38.4743
    - type: euclidean_f1
      value: 58.2994
    - type: euclidean_f1_threshold
      value: 45.4114
    - type: euclidean_precision
      value: 53.3772
    - type: euclidean_recall
      value: 64.2216
    - type: euclidean_ap
      value: 60.9374
    - type: dot_accuracy
      value: 82.2972
    - type: dot_accuracy_threshold
      value: 92.5986
    - type: dot_f1
      value: 58.2994
    - type: dot_f1_threshold
      value: 89.689
    - type: dot_precision
      value: 53.3772
    - type: dot_recall
      value: 64.2216
    - type: dot_ap
      value: 60.9374
    - type: max_accuracy
      value: 82.2972
    - type: max_f1
      value: 58.2994
    - type: max_precision
      value: 53.74830000000001
    - type: max_recall
      value: 64.2216
    - type: max_ap
      value: 60.9374
    - type: main_score
      value: 60.9374
    task:
      type: PairClassification
  - dataset:
      config: default
      name: MTEB TwitterURLCorpus (default)
      revision: 8b6510b0b1fa4e4c4f879467980e9be563ec1cdf
      split: test
      type: mteb/twitterurlcorpus-pairclassification
    metrics:
    - type: similarity_accuracy
      value: 87.2162
    - type: similarity_accuracy_threshold
      value: 91.6164
    - type: similarity_f1
      value: 74.8086
    - type: similarity_f1_threshold
      value: 90.18260000000001
    - type: similarity_precision
      value: 69.3065
    - type: similarity_recall
      value: 81.25959999999999
    - type: similarity_ap
      value: 82.53160000000001
    - type: cosine_accuracy
      value: 87.2162
    - type: cosine_accuracy_threshold
      value: 91.6164
    - type: cosine_f1
      value: 74.8086
    - type: cosine_f1_threshold
      value: 90.18260000000001
    - type: cosine_precision
      value: 69.3065
    - type: cosine_recall
      value: 81.25959999999999
    - type: cosine_ap
      value: 82.53160000000001
    - type: manhattan_accuracy
      value: 87.21039999999999
    - type: manhattan_accuracy_threshold
      value: 899.2865999999999
    - type: manhattan_f1
      value: 74.77510000000001
    - type: manhattan_f1_threshold
      value: 962.114
    - type: manhattan_precision
      value: 70.6927
    - type: manhattan_recall
      value: 79.3579
    - type: manhattan_ap
      value: 82.5262
    - type: euclidean_accuracy
      value: 87.2162
    - type: euclidean_accuracy_threshold
      value: 40.9478
    - type: euclidean_f1
      value: 74.8086
    - type: euclidean_f1_threshold
      value: 44.3112
    - type: euclidean_precision
      value: 69.3065
    - type: euclidean_recall
      value: 81.25959999999999
    - type: euclidean_ap
      value: 82.53160000000001
    - type: dot_accuracy
      value: 87.2162
    - type: dot_accuracy_threshold
      value: 91.6164
    - type: dot_f1
      value: 74.8086
    - type: dot_f1_threshold
      value: 90.18260000000001
    - type: dot_precision
      value: 69.3065
    - type: dot_recall
      value: 81.25959999999999
    - type: dot_ap
      value: 82.53160000000001
    - type: max_accuracy
      value: 87.2162
    - type: max_f1
      value: 74.8086
    - type: max_precision
      value: 70.6927
    - type: max_recall
      value: 81.25959999999999
    - type: max_ap
      value: 82.53160000000001
    - type: main_score
      value: 82.53160000000001
    task:
      type: PairClassification
pipeline_tag: sentence-similarity
---
# Granite-Embedding-125m-English

**Model Summary:**
Granite-Embedding-125m-English is a 125M parameter dense biencoder embedding model from the Granite Embeddings suite that can be used to generate high quality text embeddings. This model produces embedding vectors of size 768. Compared to most other open-source models, this model was only trained using open-source relevance-pair datasets with permissive, enterprise-friendly license, plus IBM collected and generated datasets. While maintaining competitive scores on academic benchmarks such as BEIR, this model also performs well on many enterprise use cases. This model is developed using retrieval oriented pretraining, contrastive finetuning and knowledge distillation.

- **Developers:** Granite Embedding Team, IBM
- **GitHub Repository:** [ibm-granite/granite-embedding-models](https://github.com/ibm-granite/granite-embedding-models)
- **Website**: [Granite Docs](https://www.ibm.com/granite/docs/)
- **Paper:** Coming Soon
- **Release Date**: December 18th, 2024
- **License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

**Supported Languages:** 
English.

**Intended use:** 
The model is designed to produce fixed length vector representations for a given text, which can be used for text similarity, retrieval, and search applications.

**Usage with Sentence Transformers:** 
The model is compatible with SentenceTransformer library and is very easy to use:

First, install the sentence transformers library
```shell
pip install sentence_transformers
```

The model can then be used to encode pairs of text and find the similarity between their representations

```python
from sentence_transformers import SentenceTransformer, util

model_path = "ibm-granite/granite-embedding-125m-english"
# Load the Sentence Transformer model
model = SentenceTransformer(model_path)

input_queries = [
    ' Who made the song My achy breaky heart? ',
    'summit define'
    ]

input_passages = [
    "Achy Breaky Heart is a country song written by Don Von Tress. Originally titled Don't Tell My Heart and performed by The Marcy Brothers in 1991. ",
    "Definition of summit for English Language Learners. : 1 the highest point of a mountain : the top of a mountain. : 2 the highest level. : 3 a meeting or series of meetings between the leaders of two or more governments."
    ]

# encode queries and passages
query_embeddings = model.encode(input_queries)
passage_embeddings = model.encode(input_passages)

# calculate cosine similarity
print(util.cos_sim(query_embeddings, passage_embeddings))
```

**Usage with Huggingface Transformers:** 
This is a simple example of how to use the Granite-Embedding-125m-English model with the Transformers library and PyTorch.

First, install the required libraries
```shell
pip install transformers torch
```

The model can then be used to encode pairs of text

```python
import torch
from transformers import AutoModel, AutoTokenizer

model_path = "ibm-granite/granite-embedding-125m-english"

# Load the model and tokenizer
model = AutoModel.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

input_queries = [
    ' Who made the song My achy breaky heart? ',
    'summit define'
    ]

# tokenize inputs
tokenized_queries = tokenizer(input_queries, padding=True, truncation=True, return_tensors='pt')

# encode queries
with torch.no_grad():
    # Queries
    model_output = model(**tokenized_queries)
    # Perform pooling. granite-embedding-125m-english uses CLS Pooling
    query_embeddings = model_output[0][:, 0]

# normalize the embeddings
query_embeddings = torch.nn.functional.normalize(query_embeddings, dim=1)

```
**Evaluation:**

The performance of the Granite-Embedding-125M-English model on MTEB Retrieval (i.e., BEIR) and code retrieval (CoIR) benchmarks is reported below. 

| Model                           | Paramters (M)| Embedding Dimension |  MTEB Retrieval (15) |  CoIR (10) | 
|---------------------------------|:------------:|:-------------------:|:-------------------: |:----------:|
|granite-embedding-125m-english   |125           |768                  |52.3                  |50.3        | 

**Model Architecture:**
Granite-Embedding-125m-English is based on an encoder-only RoBERTa like transformer architecture, trained internally at IBM Research.

| Model                     | granite-embedding-30m-english | granite-embedding-125m-english    | granite-embedding-107m-multilingual | granite-embedding-278m-multilingual |
| :---------                | :-------:| :--------:   | :-----:| :-----:|
| Embedding size            | 384  | **768**        | 384    | 768    |
| Number of layers          | 6    | **12**           | 6      | 12     |
| Number of attention heads | 12   | **12**          | 12     | 12     |
| Intermediate size         | 1536 | **3072**         | 1536   | 3072   |
| Activation Function       | GeLU | **GeLU**         | GeLU   | GeLU   |
| Vocabulary Size           | 50265| **50265**        | 250002 | 250002 |
| Max. Sequence Length      | 512  | **512**          | 512    | 512    |
| # Parameters              | 30M  | **125M**         | 107M   | 278M   |


**Training Data:**
Overall, the training data consists of four key sources: (1) unsupervised title-body paired data scraped from the web, (2) publicly available paired with permissive, enterprise-friendly license, (3) IBM-internal paired data targetting specific technical domains, and (4) IBM-generated synthetic data. The data is listed below:

| **Dataset**                                        | **Num. Pairs** | 
|----------------------------------------------------|:---------------:|
| SPECTER citation triplets                          | 684,100         | 
| Stack Exchange Duplicate questions (titles)        | 304,525         | 
| Stack Exchange Duplicate questions (bodies)        | 250,519         | 
| Stack Exchange Duplicate questions (titles+bodies) | 250,460         | 
| Natural Questions (NQ)                             | 100,231         | 
| SQuAD2.0                                           | 87,599          | 
| PAQ (Question, Answer) pairs                       | 64,371,441       | 
| Stack Exchange (Title, Answer) pairs               | 4,067,139        | 
| Stack Exchange (Title, Body) pairs                 | 23,978,013       | 
| Stack Exchange (Title+Body, Answer) pairs          | 187,195         | 
| S2ORC Citation pairs (Titles)                      | 52,603,982       | 
| S2ORC (Title, Abstract)                            | 41,769,185       | 
| S2ORC (Citations, abstracts)                       | 52,603,982       | 
| WikiAnswers Duplicate question pairs               | 77,427,422       | 
| SearchQA                                           | 582,261         | 
| HotpotQA                                           | 85,000          | 
| Fever                                              | 109,810         | 
| Arxiv                                              | 2,358,545        | 
| Wikipedia                                          | 20,745,403       | 
| PubMed                                             | 20,000,000       | 
| Miracl En Pairs                                    | 9,016           | 
| DBPedia Title-Body Pairs                           | 4,635,922        | 
| Synthetic: Query-Wikipedia Passage                 | 1,879,093        | 
| Synthetic: Fact Verification                       | 9,888           | 
| IBM Internal Triples                               | 40,290          | 
| IBM Internal Title-Body Pairs                      | 1,524,586        | 

Notably, we do not use the popular MS-MARCO retrieval dataset in our training corpus due to its non-commercial license, while other open-source models train on this dataset due to its high quality.

**Infrastructure:**
We train Granite Embedding Models using IBM's computing cluster, Cognitive Compute Cluster, which is outfitted with NVIDIA A100 80gb GPUs. This cluster provides a scalable and efficient infrastructure for training our models over multiple GPUs.

**Ethical Considerations and Limitations:** 
The data used to train the base language model was filtered to remove text containing hate, abuse, and profanity. Granite-Embedding-125m-English is trained only for English texts, and has a context length of 512 tokens (longer texts will be truncated to this size).

**Resources**
- ⭐️ Learn about the latest updates with Granite: https://www.ibm.com/granite
- 📄 Get started with tutorials, best practices, and prompt engineering advice: https://www.ibm.com/granite/docs/
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources

<!-- ## Citation
```
@misc{granite-embedding-models,
  author = {author 1, author2, ...},
  title = {},
  journal = {},
  volume = {},
  year = {2024},
  url = {https://arxiv.org/abs/0000.00000},
}
``` -->