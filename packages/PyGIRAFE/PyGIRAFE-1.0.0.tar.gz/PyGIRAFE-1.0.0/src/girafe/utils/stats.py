import scipy.stats as sci_stats
import numpy as np
import scikit_posthocs as sp


def compare_two_distributions(distribution1, distribution2, pvalues=0.05, verbose=True):

    # utils #
    distribution1 = np.array(distribution1)
    distribution2 = np.array(distribution2)
    length_d1 = len(distribution1)
    length_d2 = len(distribution2)
    mean_d1 = np.nanmean(distribution1)
    median_d1 = np.nanmedian(distribution1)
    median_d2 = np.nanmedian(distribution2)
    mean_d2 = np.nanmean(distribution2)
    sigma1 = np.nanstd(distribution1)
    sigma2 = np.nanstd(distribution2)
    iqr_d1 = sci_stats.iqr(distribution1, nan_policy='omit')
    iqr_d2 = sci_stats.iqr(distribution2, nan_policy='omit')

    if verbose:
        print(f"Distribution1: {length_d1} samples, mean/std: {mean_d1:.3f}/{sigma1:.3f}, "
              f"median/iqr : {median_d1:.2f}/{iqr_d1:.2f}")
        print(f"Distribution2: {length_d2} samples, mean/std: {mean_d2:.3f}/{sigma2:.3f}, "
              f"median/iqr : {median_d2:.2f}/{iqr_d2:.2f}")

    # Compare 2 distributions (are they drawn from the same distribution #
    if length_d1 < 25 or length_d2 < 25:
        if verbose:
            print(f"Small sample size")
            print(f"Use the Anderson-Darling test for distributions comparison ")
        significance_level = sci_stats.anderson_ksamp([distribution1, distribution2], midrank=True)[2]
        if verbose:
            print(f"The null hypothesis that 2 distributions are drawn from the same population can be rejected at "
                  f"{significance_level*100} % significance level")

    if length_d1 >= 25 and length_d2 >= 25:
        if verbose:
            print(f"Large enough sample size")
            print(f"Use the KS and Epps-Singleton tests for distributions comparison ")
        [ks_stat, pvalue] = sci_stats.ks_2samp(distribution1, distribution2)
        if verbose:
            if pvalue < pvalues:
                print(f" The 2 distributions are not drawn from the same continuous distribution, "
                      f"KS_2samples test, D:{ks_stat}, p-value:{pvalue}")
            if pvalue >= pvalues:
                print(f" The 2 distributions may be drawn from the same continuous distribution, "
                      f"KS_2samples test, D:{ks_stat}, p-value:{pvalue}")

        [stat, pval] = sci_stats.epps_singleton_2samp(distribution1, distribution2, t=(0.4, 0.8))
        if verbose:
            if pvalue < pvalues:
                print(f" The 2 distributions are not drawn from the same continuous distribution, "
                      f"Epps-Singleton test, D:{stat}, p-value:{pval}")
            if pvalue >= pvalues:
                print(f" The 2 distributions may be drawn from the same continuous distribution, "
                      f"Epps-Singleton test, D:{stat}, p-value:{pval}")

    # Comparaison of the means #
    if length_d1 < 30 or length_d2 < 30:
        if verbose:
            print(f"Small sample size, use non-parametric comparison of the 2 means")
        [stat, pval] = sci_stats.mannwhitneyu(distribution1, distribution2,
                                              use_continuity=True, alternative='two-sided')
        if verbose:
            print(f"Mann-Whitney sum of rank : U:{stat}, p-value:{pval}")

    if length_d1 >= 30 and length_d2 >= 30:
        if verbose:
            print(f"Large enough sample size, try parametric comparison of the 2 means")
        # test normality of each distribution #
        norm_distribution1 = (distribution1 - mean_d1) / sigma1
        norm_distribution2 = (distribution2 - mean_d2) / sigma2

        [w1, p_norm1] = sci_stats.shapiro(norm_distribution1)
        [w2, p_norm2] = sci_stats.shapiro(norm_distribution2)

        if p_norm1 > pvalues and p_norm2 > pvalues:
            if verbose:
                print(f"The 2 distributions are normally distributed, p-value1:{p_norm1}, p-value2 {p_norm2}")
                print(f"Pursue with Bartlett test for equality of variances ")
            # test equality of variances #
            [Bartlett_stat, pval_variance] = sci_stats.bartlett(distribution1, distribution2)
            if pval_variance > pvalues:
                if verbose:
                    print(f"Equality of variances is checked, p-value:{pval_variance}")
                    print(f"Requirements for classic Student-test are satisfied")
                [t_test_stat, pval_mean] = sci_stats.ttest_ind(distribution1, distribution2, axis=None,
                                                               equal_var=True, nan_policy='propagate')
                if pval_mean < pvalues:
                    if verbose:
                        print(f"The two mean are different, Student-test, T:{t_test_stat}, p-value: {pval_mean}")
                if pval_mean >= pvalues:
                    if verbose:
                        print(f"The two mean are not different, Student-test, T:{t_test_stat}, p-value: {pval_mean}")
            if pval_variance <= pvalues:
                if verbose:
                    print(f"Equality of variances is not checked, p-value:{pval_variance}")
                    print(f"Requirements for Welch modified Student-test are satisfied")
                [w_test_stat, pval_w_mean] = sci_stats.ttest_ind(distribution1, distribution2, axis=None,
                                                                 equal_var=False, nan_policy='propagate')
                if pval_w_mean < pvalues:
                    if verbose:
                        print(f"The two mean are different, Welch-student-test, T:{w_test_stat}, p-value: {pval_w_mean}")
                if pval_w_mean >= pvalues:
                    if verbose:
                        print(f"The two mean are not different, Welch-student-test, T:{w_test_stat}, p-value: {pval_w_mean}")

        if p_norm1 <= pvalues or p_norm2 <= pvalues:
            if verbose:
                print(f"At least 1 distribution is not normally distributed, p-value1:{p_norm1}, p-value2 {p_norm2}")
                print(f"Use non-parametric comparison")
            [mw_stat, p] = sci_stats.mannwhitneyu(distribution1, distribution2,
                                                  use_continuity=True, alternative='two-sided')
            if verbose:
                print(f"Mann-Whitney sum of rank : U:{mw_stat}, p-value:{p}")

    return


def multiple_comparison_one_factor_effect(distributions_list, pvalues=0.05, verbose=True, sessions_ids=None):
    do_kruskall_wallis = False
    do_one_way_anova = False
    homoscedasticity = False
    normality = False
    n_distributions = len(distributions_list)
    if verbose:
        print(f"Test the hypothesis that these {n_distributions} distributions have the same population mean or median")

    normalized_distributions_list = []
    sample_size_list = []
    for distribution_index, distribution in enumerate(distributions_list):
        normalized_distribution = (distribution - np.nanmean(distribution)) / np.nanstd(distribution)
        normalized_distributions_list.append(normalized_distribution)
        sample_size = len(distribution)
        sample_size_list.append(sample_size)
    sample_size_list = np.array(sample_size_list)

    if len(np.where(sample_size_list < 30)[0]) >= 1:
        do_kruskall_wallis = True
        if verbose:
            print(f"At least one distribution contains less than 30 samples: do Kruskall-Wallis test")

    if len(np.where(sample_size_list < 30)[0]) == 0:
        if verbose:
            print(f"All distributions contain more than 30 samples: check one-way ANOVA requirements")

        # Test the 2 requirements for one-way ANOVA: normality and homoscedasticity #
        pvalues_normality = []
        for distribution_index, normalized_distribution in enumerate(normalized_distributions_list):
            pvalue_norm = sci_stats.shapiro(normalized_distribution)[1]
            pvalues_normality.append(pvalue_norm)
        pvalues_normality = np.array(pvalues_normality)

        if len(np.where(pvalues_normality <= pvalues)[0]) >= 1:
            normality = False
            if verbose:
                print(f"At least one distribution is not normally distributed.")
        if len(np.where(pvalues_normality <= pvalues)[0]) == 0:
            normality = True
            if verbose:
                print(f"All distributions are normally distributed")

        pvalue_variances = sci_stats.bartlett(*distributions_list)[1]
        if pvalue_variances <= pvalues:
            homoscedasticity = False
            if verbose:
                print(f"All distributions do not share the same variance.")
        if pvalue_variances > pvalues:
            homoscedasticity = True
            if verbose:
                print(f"Homoscedasticity is verified")

    if homoscedasticity is True and normality is True:
        do_one_way_anova = True
        if verbose:
            print(f"Normality and homoscedasticity are verified: do one-way ANOVA")
    if homoscedasticity is False or normality is False:
        do_kruskall_wallis = True
        if verbose:
            print(f"Normality and homoscedasticity are not verified: do Kruskall-Wallis test")

    if do_kruskall_wallis:
        [kw, pvalue] = sci_stats.kruskal(*distributions_list, nan_policy='omit')
        if pvalue >= pvalues:
            if verbose:
                print(f"Population median of all of the groups are equal, KW-value:{kw}, p-value:{pvalue}")
        if pvalue < pvalues:
            if verbose:
                print(f"At least one group as a population median that differs, KW-value:{kw}, p-value:{pvalue}")
                print(f"Perform Dunn's test with Bonferroni correction")
            pvalues = sp.posthoc_dunn(distributions_list, p_adjust='bonferroni')
            if verbose:
                print(f"Sessions ids: {sessions_ids}")
                print(f"pvalues table: ")
                print(f"{pvalues}")

    if do_one_way_anova:
        [f, pval] = sci_stats.f_oneway(*distributions_list)
        if pval >= pvalues:
            if verbose:
                print(f"Population median of all of the groups are equal, F-value:{f}, p-value:{pval}")
        if pval < pvalues:
            if verbose:
                print(f"At least one group as a population median that differs, F-value:{f}, p-value:{pval}")
                print(f"Perform Student's test with Holm correction")
            pvalues_posthoc = sp.posthoc_ttest(distributions_list, p_adjust='holm')
            if verbose:
                print(f"Sessions ids: {sessions_ids}")
                print(f"pvalues table: ")
                print(f"{pvalues_posthoc}")

    return

