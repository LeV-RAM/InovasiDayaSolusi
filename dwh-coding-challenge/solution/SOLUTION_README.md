# Summary
For this problem, I firstly create the functions to find and read the .JSON files. I also created a function to obtain the parameters and values of each .JSON files. For context, I have moved the 'data' folder into the 'solution' folder to ease the calling of file directory. 

- For Task 1, I declared the dataframes for each category (accounts, cards, savings) and display them in tables. For a better view, I replaced the 'NaN' values with '-' to show empty values.
- For Task 2, I merged the accounts table with the cards table based on 'card_id', and then joinned the new table with the sabings_accounts table based on the savings_account_id. Finally, I displayed the final table afterwards. This requires more improvement in the arrangement aspect since I believe data analysis requires a more appearant and clear data.
- For Task 3, I summed the number of transactions based on the joinned table. If there exists a transaction, it will display its details including the timestamp.

I also added automations scripts, specifically for building / re-building the docker along with the required libraries and running them respectively.