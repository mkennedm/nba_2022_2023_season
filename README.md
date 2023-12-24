# Visualizations
This report contains two pages of visualizations based on data from the 2022-2023 National Basketball Association season. The first page focuses on players.

Users can select as many players as they want to compare them in a clustered column chart with columns for average points, offensive rebounds, defensive rebounds, assists, and their Player Efficiency Rating (PER). For players who were on more than one team throughout the season, the data set contained one entry for each team they were on. This allows users to compare how a single player performed before and after a mid-season trade.

A pie chart on the same page shows the number of field goals made by the selected player(s) that were 3-pointers compared to 2-pointers.

![player_statistics](https://github.com/mkennedm/nba_2022_2023_season/assets/8769212/1221e868-84f7-4bb7-a931-3a6a3247219a)


At the bottom of the page, there’s a scatter chart with field goal percentage as the Y-axis and points per game as the X-axis. The scatter chart without any filtering is pictured below.

![scatterplot](https://github.com/mkennedm/nba_2022_2023_season/assets/8769212/035581ca-1725-4a50-802b-16b99ccd925d)


The second page focuses on teams. All visualizations on this page include data for all teams and can be filtered to show only a desired subset.

I imported the radar chart visual to display team wide stats for adjusted offensive rating (defined by Basketball Reference as “An estimate of points scored per 100 possessions adjusted for strength of opponent defense.”), adjusted defensive rating (same as before except for points allowed instead of points scored), points per game, total (offensive and defensive) rebounds per game, field goals per game, and total number of wins over the course of the season.

![radar_chart](https://github.com/mkennedm/nba_2022_2023_season/assets/8769212/41d37830-d889-4624-ade6-11c8a0daab54)


There’s a line chart that shows the number of points each team earned in each game of the season. Hovering over a single point will show the opposing team’s name and score for the same game.

![line_chart](https://github.com/mkennedm/nba_2022_2023_season/assets/8769212/9a64a42d-6745-449d-add3-efd073a63558)


Finally, there’s a heatmap for wins against each team in the NBA. A dark blue cell in the heat map means the team in that row of the matrix has a relatively high number of wins against the team in that column.

![heatmap](https://github.com/mkennedm/nba_2022_2023_season/assets/8769212/36196b89-5388-463d-abf1-6f6d268bc5f9)

Watch a video of the published report here:


https://github.com/mkennedm/nba_2022_2023_season/assets/8769212/b089c3d4-704f-4e6b-b731-54995fda3d9f




# Data Collection
This section covers only the tables that were not created within Power BI.

## Games
The Games table was originally created by exporting CSV files from Basketball Reference. The website has one page for each month of the season which gave me 9 CSVs (October 2022 up to and including June 2023). I saved all the CSVs in the same folder and imported the entire folder to make the Games table. This table includes one row for each game of the season and provides game’s date, the visiting team, home team, each team’s score, among other information. 

## Games by Team
I created Games by Team in Python by modifying the data from Games. This was needed because I wanted to be able to filter the Teams page by each team. The format of the Games table from Basketball Reference allowed filtering by home team and visiting team. This does not lend itself well to visualizing a single team’s entire season because for some games, the team will appear in the home column and in the visiting column for other games. Games by Team has a Team column and an Opponent column which means filtering by Team will show all of the games for a given team regardless of whether it was a home or away game. This also required two rows for each game. For example, the Houston Rockets played against the Memphis Grizzlies on October 21st, 2022. In one row, the Rockets are in the Team column and the Grizzlies are in the Opponent column. In another row, the Grizzlies are in the Team column and the Rockets are in the Opponent column.

Due to the nature of the transformation, I found it simpler to use Python code to generate this data. I first combined the 9 CSVs used to create the Games table with the combine_CSVs function in create_CSVs.py. This function takes in the name of a folder and a file destination as inputs. It turns all of the files in the folder into Pandas DataFrames and combines all of the DataFrames into one big DataFrame before outputting this larger DataFrame in a single CSV. I ran create_CSVs with the name of the folder containing the CSV files and all_games.csv as the file destination.

Next I used get_games_by_team to import all_games.csv as a DataFrame, drop unnecessary columns then rename and reorder some of the remaining columns. After that, a new CSV file called games_by_team.csv was created. This has all of the rows from the DataFrame plus additional rows where the values for the Team, Team Score, Opponent, and Opponent Score columns were swapped.

Next, I uploaded games_by_team.csv to Power BI and performed a few more operations with Power Query. The most complicated of these was adding a Win column that has a value of 1 when Team has more points than Opponent and 0 otherwise. Defined below.

`= Table.AddColumn(#"Changed Type1", "Win", each if [Team Score] > [Opponent Score] then 1 else 0)`

This column is used in the heat map visualization.

## Players
The Players table came from Basketball Reference’s Player Per Game table exported from the website as a CSV then imported into Power BI.

## Players Advanced
The Players Advanced table came from Basketball Reference’s Player Advanced table exported from the website as a CSV then imported into Power BI.

## Teams
The Teams table was imported directly from the webpage Wikipedia:WikiProject National Basketball Association/National Basketball Association team abbreviations. The column names were changed to Abbreviation and Full Name.

## Team Averages
The Team Averages table came from Basketball Reference’s 2022-2023 season Per Game table for all teams. The table was exported from the website as a CSV then imported into Power BI.

## Team Ratings
The Team Ratings table from Basketball Reference’s 2022-2023 season Team Ratings table. The table was exported from the website as a CSV then imported into Power BI.

# Data Modeling

## Date

I created the Date table early on since the Games table came with a Date column. I wanted to have a single table for just dates in case I decided to add any future tables with date data and wanted to be able to sort or filter based on dates. The table was created with the following DAX formula.

```
Date =
VAR MinDate =  MIN ( Games[Date] )
VAR MaxDate = MAX ( Games[Date] )
RETURN
ADDCOLUMNS (
    FILTER (
        CALENDARAUTO( ),
        AND (  [Date]  >= MinDate, [Date] <= MaxDate )
    ),
    "Calendar Year", "CY " & YEAR ( [Date] ),
    "Month Name", FORMAT ( [Date], "mmmm" ),
    "Month Number", MONTH ( [Date] )
)
```

## Team Radar Table
The Team Radar Table was created to make use of the radar chart. Columns from Team Ratings and Team Averages (Field Goals, Total Rebounds, Points, Wins, Adjusted Offensive Rating, and Adjusted Defensive Rating) were converted into rows making six rows per team.

This table was created in Power Query using the steps below.

```
let
	Source = Table.NestedJoin(#"Team Averages", {"Team"}, #"Team Ratings", {"Team"}, "Team Ratings", JoinKind.Inner),
	#"Expanded Team Ratings" = Table.ExpandTableColumn(Source, "Team Ratings", {"Conf", "Div", "W", "L", "W/L%", "MOV", "ORtg", "DRtg", "NRtg", "MOV/A", "ORtg/A", "DRtg/A", "NRtg/A"}, {"Conf", "Div", "W", "L", "W/L%", "MOV", "ORtg", "DRtg", "NRtg", "MOV/A", "ORtg/A", "DRtg/A", "NRtg/A"}),
	#"Removed Other Columns" = Table.SelectColumns(#"Expanded Team Ratings",{"Team", "FG", "TRB", "PTS", "W", "ORtg/A", "DRtg/A"}),
	#"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Removed Other Columns", {"Team"}, "Attribute", "Value"),
	#"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Category"}, {"Value", "Average"}}),
	#"Replaced Value" = Table.ReplaceValue(#"Renamed Columns","ORtg/A","Adjusted Offensive Rating",Replacer.ReplaceText,{"Category"}),
	#"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","TRB","Total Rebounds",Replacer.ReplaceText,{"Category"}),
	#"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","PTS","Points",Replacer.ReplaceText,{"Category"}),
	#"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","W","Wins",Replacer.ReplaceText,{"Category"}),
	#"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","FG","Field Goals",Replacer.ReplaceText,{"Category"}),
	#"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","DRtg/A","Adjusted Defensive Rating",Replacer.ReplaceText,{"Category"})
in
	#"Replaced Value5"
```

# Relationships

| Table 1          | Table 1 Column Name | Cardinality  | Table 2          | Table 2 Column Name |
|------------------|---------------------|--------------|------------------|---------------------|
| Games by Team    | Date                | Many to one  | Date             | Date                |
| Games            | Date                | Many to one  | Date             | Date                |
| Games            | Visitor/Neutral     | Many to one  | Teams            | Full Name           |
| Games            | Home/Neutral        | Many to one  | Teams            | Full Name           |
| Games by Team    | Team                | Many to one  | Teams            | Full Name           |
| Games by Team    | Opponent            | Many to one  | Teams            | Full Name           |
| Players          | Tm                  | Many to one  | Teams            | Abbreviation        |
| Players          | Player-additional   | Many to many | Players Advanced | Player-additional   |
| Players Advanced | Tm                  | Many to one  | Teams            | Abbreviation        |
| Team Averages    | Team                | One to one   | Teams            | Full Name           |
| Team Radar Table | Team                | Many to one  | Teams            | Full Name           |
| Team Ratings     | Team                | One to one   | Teams            | Full Name           |
