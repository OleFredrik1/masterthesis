# Log Fold Change calculations
python Scripts/LogFoldChange/log_fold_change_corr_strat.py && cp Outdata/log_fold_change_corr_strat.csv ../Masterthesis/tables/LogFoldChange/log_fold_change_corr_strat.csv &
python Scripts/LogFoldChange/log_fold_change_corr_strat_rand.py && cp Outdata/log_fold_change_corr_strat_rand.csv ../Masterthesis/tables/LogFoldChange/log_fold_change_corr_strat_rand.csv &
python Scripts/LogFoldChange/log_fold_change_corr_strat_pvalue_log.py && cp Outdata/log_fold_change_corr_strat_pvalue_log.csv ../Masterthesis/tables/LogFoldChange/log_fold_change_corr_strat_pvalue_log.csv &
python Scripts/LogFoldChange/log_fold_change_corr_strat_all.py && cp Outdata/log_fold_change_corr_strat_all.csv ../Masterthesis/tables/LogFoldChange/log_fold_change_corr_strat_all.csv &
python Scripts/LogFoldChange/log_fold_change_corr_strat_pvalue_diff.py && cp Outdata/log_fold_change_corr_strat_pvalue_diff.csv ../Masterthesis/tables/LogFoldChange/log_fold_change_corr_strat_pvalue_diff.csv &
python Scripts/LogFoldChange/log_fold_change_correlation_late.py && cp Outdata/log_fold_change_correlation_late.csv ../Masterthesis/tables/LogFoldChange/log_fold_change_correlation_late.csv &

# Consistent expression
python Scripts/ConsistentExpression/mirna_consistent_expression.py && cp Outdata/mirna_consistent_expression.csv ../Masterthesis/tables/ConsistentExpression/mirna_consistent_expression.csv &
python Scripts/ConsistentExpression/mirna_consistent_expression_strat.py && cp Outdata/mirna_consistent_expression_strat.csv ../Masterthesis/tables/ConsistentExpression/mirna_consistent_expression_strat.csv &
python Scripts/ConsistentExpression/mirna_consistent_expression_pvalues.py && cp Outdata/mirna_consistent_expression_pvalues.csv ../Masterthesis/tables/ConsistentExpression/mirna_consistent_expression_pvalues.csv &

# Signed Rank
python Scripts/SignedRank/signed_rank.py && cp Outdata/signed_rank.csv ../Masterthesis/tables/SignedRank/signed_rank.csv &
python Scripts/SignedRank/signed_rank_cv.py && cp Outdata/signed_rank_cv.csv ../Masterthesis/tables/SignedRank/signed_rank_cv.csv &
python Scripts/SignedRank/signed_rank_cv_tvalue.py && cp Outdata/signed_rank_cv_tvalue.csv ../Masterthesis/tables/SignedRank/signed_rank_cv_tvalue.csv &
python Scripts/SignedRank/signed_rank_cv_significant.py && cp Outdata/signed_rank_cv_significant.csv ../Masterthesis/tables/SignedRank/signed_rank_cv_significant.csv &

# Separate datasets
python Scripts/separate_datasets.py && cp Outdata/separate_datasets.csv ../Masterthesis/tables/separate_datasets.csv &

# Machine Learning Single
python Scripts/machine_learning_single.py && cp Outdata/machine_learning_single.csv ../Masterthesis/tables/machine_learning_single.csv &

# Single miRNA
python Scripts/SinglemiRNA/mirna_cohensd.py && cp Outdata/mirna_cohensd.csv ../Masterthesis/tables/SinglemiRNA/mirna_cohensd.csv &
python Scripts/SinglemiRNA/mirna_auc.py && cp Outdata/mirna_auc.csv ../Masterthesis/tables/SinglemiRNA/mirna_auc.csv &

# PCA
python Scripts/PCA/pca_asakura_fehlmann.py && cp Outdata/pca_asakura_fehlmann_asakura.csv ../Masterthesis/tables/PCA/pca_asakura_fehlmann_asakura.csv && cp Outdata/pca_asakura_fehlmann_fehlmann.csv ../Masterthesis/tables/PCA/pca_asakura_fehlmann_fehlmann.csv &
python Scripts/PCA/pca_asakura_external.py && cp Outdata/pca_asakura_external.csv ../Masterthesis/tables/PCA/pca_asakura_external.csv &
python Scripts/PCA/pca_remove_two.py && cp -R Outdata/PCA/RemoveTwo ../Masterthesis/tables/PCA/RemoveTwo &

# Common cross validation
python Scripts/common_cross_validation.py && cp Outdata/common_cross_validation.csv ../Masterthesis/tables/common_cross_validation.csv &

# Tripple train
python Scripts/Tripple/tripple_train.py && cp Outdata/tripple_single.csv ../Masterthesis/tables/Tripple/tripple_single.csv && cp Outdata/tripple_double.csv ../Masterthesis/tables/Tripple/tripple_double.csv &
python Scripts/Tripple/tripple_train_xgboost.py && cp Outdata/tripple_single_xgb.csv ../Masterthesis/tables/Tripple/tripple_single_xgb.csv && cp Outdata/tripple_double_xgb.csv ../Masterthesis/tables/Tripple/tripple_double_xgb.csv &

# Merging all
python Scripts/auc_merged.py && cp Outdata/merged_auc.csv ../Masterthesis/tables/merged_auc.csv &

# Maximal set
python Scripts/auc_maximal.py && cp Outdata/auc_maximal.csv ../Masterthesis/tables/auc_maximal.csv &

# Stratification
python Scripts/Stratification/auc_body_fluid_cv.py && cp Outdata/auc_body_fluid_cv.csv ../Masterthesis/tables/Stratification/auc_body_fluid_cv.csv &
python Scripts/Stratification/auc_body_fluid_pairs.py && cp Outdata/auc_body_fluid_pairs.csv ../Masterthesis/tables/Stratification/auc_body_fluid_pairs.csv &
python Scripts/Stratification/auc_merged_stages.py && cp Outdata/auc_merged_stages.csv ../Masterthesis/tables/Stratification/auc_merged_stages.csv &
python Scripts/Stratification/auc_microarray_cv.py && cp Outdata/auc_microarray_cv.csv ../Masterthesis/tables/Stratification/auc_microarray_cv.csv &
python Scripts/Stratification/auc_microarray_pairs.py && cp Outdata/auc_microarray_pairs.csv ../Masterthesis/tables/Stratification/auc_microarray_pairs.csv &
python Scripts/Stratification/auc_stages_pairs.py && cp Outdata/auc_stages_pairs.csv ../Masterthesis/tables/Stratification/auc_stages_pairs.csv &
python Scripts/Stratification/auc_technology_cv.py && cp Outdata/auc_technology_cv.csv ../Masterthesis/tables/Stratification/auc_technology_cv.csv &
python Scripts/Stratification/auc_technology_pairs.py && cp Outdata/auc_technology_pairs.csv ../Masterthesis/tables/Stratification/auc_technology_pairs.csv &
python Scripts/Stratification/auc_histogram_cv.py && cp Outdata/auc_histogram_cv_microarray.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_microarray.csv && cp Outdata/auc_histogram_cv_sequencing.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_sequencing.csv && cp Outdata/auc_histogram_cv_qrt-pcr.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_qrt-pcr.csv && cp Outdata/auc_histogram_cv_serum.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_serum.csv && cp Outdata/auc_histogram_cv_plasma.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_plasma.csv && cp Outdata/auc_histogram_cv_whole_blood.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_whole_blood.csv && cp Outdata/auc_histogram_cv_all.csv ../Masterthesis/tables/Stratification/auc_histogram_cv_all.csv && cp Outdata/auc_qqplot_cv.pdf ../Masterthesis/figs/auc_qqplot_cv.pdf &


# Hierarchial clustering
python Scripts/Clustering/hierarchical_clustering_datasets.py && cp Outdata/hierarchical_clustering_datasets.pdf ../Masterthesis/figs/hierarchical_clustering_datasets.pdf &
python Scripts/Clustering/hierarchical_clustering_pairs.py && cp Outdata/hierarchical_clustering_pairs.csv ../Masterthesis/tables/Clustering/hierarchical_clustering_pairs.csv &
python Scripts/Clustering/hierarchical_clustering_merged.py && cp Outdata/hierarchical_clustering_merged.csv ../Masterthesis/tables/Clustering/hierarchical_clustering_merged.csv &

# PCA Cross Validate
python Scripts/PCACrossValidate/pca_cross_validate.py && cp Outdata/pca_cross_validate_pca.csv ../Masterthesis/tables/PCACrossValidate/pca_cross_validate_pca.csv && cp Outdata/pca_cross_validate_no_pca.csv ../Masterthesis/tables/PCACrossValidate/pca_cross_validate_no_pca.csv &

# Prediction correlation
python Scripts/asakura_predictions_correlation.py && cp Outdata/asakura_predictions_correlation.pickle ../Masterthesis/tables/asakura_predictions_correlation.pickle &
python Scripts/predictions_correlation.py && cp Outdata/predictions_correlation.pickle ../Masterthesis/tables/predictions_correlation.pickle &

# Test removing mean fold change
python Scripts/auc_zero_mean_fold_change.py && cp Outdata/auc_zero_mean_fold_change.csv ../Masterthesis/tables/auc_zero_mean_fold_change.csv &

# AUC PCA
python Scripts/auc_pca_t_test.py && cp Outdata/auc_pca_t_test.csv ../Masterthesis/tables/auc_pca_t_test.csv &

# Sequence threshold
python Scripts/rpm_threshold_cv.py && cp Outdata/rpm_threshold_cv.csv ../Masterthesis/tables/rpm_threshold_cv.csv &
python Scripts/rpm_threshold_auc.py && cp Outdata/rpm_threshold_auc.csv ../Masterthesis/tables/rpm_threshold_auc.csv && cp Outdata/rpm_threshold_auc_pvalue.csv ../Masterthesis/tables/rpm_threshold_auc_pvalue.csv &

# Red blood cells
python Scripts/RedBloodCells/relative_expression.py && cp Outdata/relative_expression.csv ../Masterthesis/tables/RedBloodCells/relative_expression.csv &
python Scripts/RedBloodCells/relative_expression_interval.py && cp Outdata/relative_expression_interval.csv ../Masterthesis/tables/RedBloodCells/relative_expression_interval.csv &
python Scripts/RedBloodCells/relative_expression_body_fluid.py && cp Outdata/relative_expression_body_fluid.csv ../Masterthesis/tables/RedBloodCells/relative_expression_body_fluid.csv &
python Scripts/RedBloodCells/relative_variance.py && cp Outdata/relative_variance.csv ../Masterthesis/tables/RedBloodCells/relative_variance.csv &
python Scripts/RedBloodCells/relative_variance_body_fluid.py && cp Outdata/relative_variance_body_fluid.csv ../Masterthesis/tables/RedBloodCells/relative_variance_body_fluid.csv &

python Scripts/study_table.py && cp Outdata/study_table.csv ../Masterthesis/tables/study_table.csv &

wait
echo "Done!"