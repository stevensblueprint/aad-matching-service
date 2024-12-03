import pandas as pd


# TODO: If a user puts an invalid KIN ID, just remove from preferences list and add an additional ID to auto-generate
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
        raw_data_df.columns[5]: "id",  # Participant ID
        raw_data_df.columns[10]: "rank_1",  # First common rank question
        raw_data_df.columns[11]: "rank_2",  # Second common rank question
        raw_data_df.columns[12]: "rank_3",  # Third common rank question
        raw_data_df.columns[13]: "rank_4",  # Fourth common rank question
        raw_data_df.columns[14]: "mentor_or_mentee",  # Mentor or Mentee
    }

    # Step 2: Process Mentor and Mentee-specific columns
    column_mapping_mentor = {
        raw_data_df.columns[15]: "multiple_mentors",  # Multiple mentors
        raw_data_df.columns[16]: "industry",  # Industry column for mentors
        raw_data_df.columns[17]: "rank_5",  # Fifth rank question for mentors
        raw_data_df.columns[18]: "rank_6",  # Sixth rank question for mentors
        raw_data_df.columns[19]: "preference_1",  # First preference for mentors
        raw_data_df.columns[20]: "preference_2",  # Second preference for mentors
        raw_data_df.columns[21]: "preference_3",  # Third preference for mentors
        raw_data_df.columns[22]: "preference_4",  # Fourth preference for mentors
        raw_data_df.columns[23]: "preference_5",  # Fifth preference for mentors
        raw_data_df.columns[24]: "preference_6",  # Sixth preference for mentors
        raw_data_df.columns[25]: "preference_7",  # Seventh preference for mentors
        raw_data_df.columns[26]: "preference_8",  # Eighth preference for mentors
        raw_data_df.columns[27]: "preference_9",  # Ninth preference for mentors
        raw_data_df.columns[28]: "preference_10",  # Tenth preference for mentors
        raw_data_df.columns[29]: "preference_11",  # Eleventh preference for mentors
        raw_data_df.columns[30]: "preference_12",  # Twelfth preference for mentors
        raw_data_df.columns[31]: "preference_13",  # Thirteenth preference for mentors
        raw_data_df.columns[32]: "preference_14",  # Fourteenth preference for mentors
        raw_data_df.columns[33]: "preference_15",  # Fifteenth preference for mentors
    }

    column_mapping_mentee = {
        raw_data_df.columns[34]: "multiple_mentees",  # Multiple mentees
        raw_data_df.columns[35]: "industry",  # Industry column for mentees
        raw_data_df.columns[36]: "rank_5",  # Fifth rank question for mentees
        raw_data_df.columns[37]: "rank_6",  # Sixth rank question for mentees
        raw_data_df.columns[38]: "preference_1",  # First preference for mentees
        raw_data_df.columns[39]: "preference_2",  # Second preference for mentees
        raw_data_df.columns[40]: "preference_3",  # Third preference for mentees
        raw_data_df.columns[41]: "preference_4",  # Fourth preference for mentees
        raw_data_df.columns[42]: "preference_5",  # Fifth preference for mentees
        raw_data_df.columns[43]: "preference_6",  # Sixth preference for mentees
        raw_data_df.columns[44]: "preference_7",  # Seventh preference for mentees
        raw_data_df.columns[45]: "preference_8",  # Eighth preference for mentees
        raw_data_df.columns[46]: "preference_9",  # Ninth preference for mentees
        raw_data_df.columns[47]: "preference_10",  # Tenth preference for mentees
        raw_data_df.columns[48]: "preference_11",  # Eleventh preference for mentees
        raw_data_df.columns[49]: "preference_12",  # Twelfth preference for mentees
        raw_data_df.columns[50]: "preference_13",  # Thirteenth preference for mentees
        raw_data_df.columns[51]: "preference_14",  # Fourteenth preference for mentees
        raw_data_df.columns[52]: "preference_15",  # Fifteenth preference for mentees
    }

    raw_data_df = raw_data_df.rename(columns=column_mapping_common)

    # TODO: maybe rename Kin Mentor to 'mentor' and Kin Mentee to 'mentee'
    mentors = raw_data_df[raw_data_df["mentor_or_mentee"] == "Kin Mentor"].copy()
    mentees = raw_data_df[raw_data_df["mentor_or_mentee"] == "Kin Mentee"].copy()

    mentors = mentors.rename(columns=column_mapping_mentor)
    mentees = mentees.rename(columns=column_mapping_mentee)
    # Combine mentor and mentee data with the same schema
    combined_data = pd.concat([mentors, mentees], ignore_index=True)

    # Retain the desired schema order
    schema_columns = (
        ["id", "mentor_or_mentee"]
        + [f"preference_{i}" for i in range(1, 16)]
        + ["industry"]
        + [f"rank_{i}" for i in range(1, 7)]
    )
    combined_data = combined_data[schema_columns]

    # Step 3: Save the processed data to a CSV file
    combined_data.to_csv("processed_data.csv", index=False)
    print("Processed data saved to 'processed_data.csv'.")


if __name__ == "__main__":
    # Provide the path to your raw form data CSV file
    process_form_data("matching_responses.csv")
