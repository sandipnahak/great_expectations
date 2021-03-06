from great_expectations.core.usage_statistics.anonymizers.anonymizer import Anonymizer
from great_expectations.dataset import Dataset

GE_EXPECTATION_TYPES = [
    el for el in Dataset.__dict__.keys() if el.startswith("expect_")
]


class ExpectationSuiteAnonymizer(Anonymizer):
    def __init__(self, salt=None):
        super().__init__(salt=salt)
        self._ge_expectation_types = GE_EXPECTATION_TYPES

    def anonymize_expectation_suite_info(self, expectation_suite):
        anonymized_info_dict = dict()
        anonymized_expectation_counts = dict()

        expectations = expectation_suite.expectations
        expectation_types = [
            expectation.expectation_type for expectation in expectations
        ]
        for expectation_type in set(expectation_types):
            if expectation_type in self._ge_expectation_types:
                anonymized_expectation_counts[
                    expectation_type
                ] = expectation_types.count(expectation_type)
            else:
                anonymized_expectation_type = self.anonymize(expectation_type)
                anonymized_expectation_counts[
                    anonymized_expectation_type
                ] = expectation_types.count(expectation_type)

        anonymized_info_dict["anonymized_name"] = self.anonymize(
            expectation_suite.expectation_suite_name
        )
        anonymized_info_dict["expectation_count"] = len(expectations)
        anonymized_info_dict[
            "anonymized_expectation_type_counts"
        ] = anonymized_expectation_counts

        return anonymized_info_dict
