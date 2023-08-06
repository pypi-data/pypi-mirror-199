from heart_model.config.core import config


def test_temporal_variable_transformer(sample_input_data):
    # Given
    assert sample_input_data["Gender"].iat[3] == "Female"
    assert sample_input_data["glucose"].iat[7] == 78

    # When
    subject_1 = sample_input_data.copy()
    subject_1.rename(columns=config.model_config.variables_to_rename, inplace=True)
    subject_2 = subject_1.copy()
    subject_2.drop(labels=config.model_config.variables_to_drop, axis=1, inplace=True)

    # Then

    # test 2
    test_subject_2 = subject_2
    assert "Gender" not in test_subject_2
    assert "education" not in test_subject_2
    assert "prevalentStroke" not in test_subject_2
