import pandas as pd

# TODO: Try-Catch to handle and highlight errors
# TODO: IDs should be retained from end to end to ensure consistency
# TODO: keep all column names lowercase with underscores for consistency


def process_form_data(form_data_path):
    """
    Process the raw form data into a format that can be used in the Gale-Shapley algorithm,
    accommodating different column setups for mentors and mentees.

    Parameters:
        form_data_path (str): Path to the raw form data CSV file.

    Output:
        A processed CSV file (`processed_data.csv`) containing the data formatted for the Gale-Shapley algorithm.
    """
    # Load the raw form data
    raw_data_df = pd.read_csv(form_data_path)

    # Step 1: Retain common columns
    column_mapping_common = {
        raw_data_df.columns[5]: "id",
        raw_data_df.columns[9]: "gender",
        raw_data_df.columns[10]: "gender_preference",
        raw_data_df.columns[11]: "rank_1",
        raw_data_df.columns[12]: "rank_2",
        raw_data_df.columns[13]: "rank_3",
        raw_data_df.columns[14]: "rank_4",
        raw_data_df.columns[15]: "mentor_or_mentee",
    }

    # Step 2: Process Mentor and Mentee-specific columns
    column_mapping_mentor = {
        raw_data_df.columns[16]: "multiple_mentors",
        raw_data_df.columns[17]: "industry",
        raw_data_df.columns[18]: "rank_5",
        raw_data_df.columns[19]: "rank_6",
        raw_data_df.columns[20]: "preference_1",
        raw_data_df.columns[21]: "preference_2",
        raw_data_df.columns[22]: "preference_3",
        raw_data_df.columns[23]: "preference_4",
        raw_data_df.columns[24]: "preference_5",
        raw_data_df.columns[25]: "preference_6",
        raw_data_df.columns[26]: "preference_7",
        raw_data_df.columns[27]: "preference_8",
        raw_data_df.columns[28]: "preference_9",
        raw_data_df.columns[29]: "preference_10",
        raw_data_df.columns[30]: "preference_11",
        raw_data_df.columns[31]: "preference_12",
        raw_data_df.columns[32]: "preference_13",
        raw_data_df.columns[33]: "preference_14",
        raw_data_df.columns[34]: "preference_15",
    }

    column_mapping_mentee = {
        raw_data_df.columns[35]: "multiple_mentees",
        raw_data_df.columns[36]: "industry",
        raw_data_df.columns[37]: "rank_5",
        raw_data_df.columns[38]: "rank_6",
        raw_data_df.columns[39]: "preference_1",
        raw_data_df.columns[40]: "preference_2",
        raw_data_df.columns[41]: "preference_3",
        raw_data_df.columns[42]: "preference_4",
        raw_data_df.columns[43]: "preference_5",
        raw_data_df.columns[44]: "preference_6",
        raw_data_df.columns[45]: "preference_7",
        raw_data_df.columns[46]: "preference_8",
        raw_data_df.columns[47]: "preference_9",
        raw_data_df.columns[48]: "preference_10",
        raw_data_df.columns[49]: "preference_11",
        raw_data_df.columns[50]: "preference_12",
        raw_data_df.columns[51]: "preference_13",
        raw_data_df.columns[52]: "preference_14",
        raw_data_df.columns[53]: "preference_15",
    }

    raw_data_df = raw_data_df.rename(columns=column_mapping_common)

    mentors = raw_data_df[raw_data_df["mentor_or_mentee"] == "Kin Mentor"].copy()
    mentees = raw_data_df[raw_data_df["mentor_or_mentee"] == "Kin Mentee"].copy()

    mentors["mentor_or_mentee"] = "mentor"
    mentees["mentor_or_mentee"] = "mentee"

    mentors = mentors.rename(columns=column_mapping_mentor)
    mentees = mentees.rename(columns=column_mapping_mentee)

    # Sort By ID
    mentors = mentors.sort_values(by="id")
    mentees = mentees.sort_values(by="id")

    # Combine mentor and mentee data with the same schema
    combined_data = pd.concat([mentors, mentees], ignore_index=True)

    # Retain the desired schema order
    schema_columns = (
        [
            "id",
            "mentor_or_mentee",
        ]
        + [f"preference_{i}" for i in range(1, 16)]
        + ["industry"]
        + [f"rank_{i}" for i in range(1, 7)]
        + ["gender", "gender_preference"]
    )
    combined_data = combined_data[schema_columns]

    # Convert all float values to int for the algorithm
    for i in range(1, 16):
        combined_data[f"preference_{i}"] = combined_data[f"preference_{i}"].astype(int)

    for i in range(1, 7):
        combined_data[f"rank_{i}"] = combined_data[f"rank_{i}"].astype(int)

    # Step 3: Save the processed data to a CSV file
    combined_data.to_csv("processed_data.csv", index=False)
    print("Processed data saved to 'processed_data.csv'.")


if __name__ == "__main__":
    # Provide the path to your raw form data CSV file
    process_form_data("matching_responses.csv")
