# YouTube Performance Power BI Dashboard

This Power BI dashboard is designed for your **YouTube Video Performance Predictor & Audience Insights System** project. It visualizes key performance metrics, temporal trends, and audience engagement insights from your YouTube dataset (`Aggregated_Metrics_By_Video.csv` and `Daily_Views_Over_Time.csv`). The dashboard is interactive, allowing content creators to filter by date, video, or other dimensions to optimize content strategies.

## Dashboard Overview
- **Purpose**: Enable content creators to analyze YouTube video performance (e.g., views, subscribers, revenue) and derive actionable insights for content optimization, such as optimal posting times and high-engagement videos.
- **Data Sources**:
  - `Aggregated_Metrics_By_Video.csv`: Video-level metrics (e.g., `Views`, `Likes`, `Subscribers gained`, `RPM (USD)`, `Publish Day`, `Publish Hour`, `subscribers_per_view`).
  - `Daily_Views_Over_Time.csv`: Aggregated daily views for time-series analysis.
- **Design Principles** (inspired by Windsor.ai and Coupler.io):[](https://windsor.ai/power-bi-youtube-dashboard/)[](https://blog.coupler.io/youtube-analytics-to-power-bi/)
  - **Simplicity**: Clear visuals with minimal clutter for quick insights.
  - **Interactivity**: Slicers and cross-filtering for data exploration.
  - **YouTube-Specific Metrics**: Focus on views, engagement, and subscriber conversion.
  - **Aesthetics**: YouTube’s color palette (red `#FF0000`, white `#FFFFFF`, black `#000000`).

## ASCII Art Mockup
Below is an ASCII representation of the dashboard layout (16:9 aspect ratio, single page). It approximates the placement of visuals and slicers.

```
+---------------------------------------------------------------+
| YouTube Video Performance Dashboard                            |
|---------------------------------------------------------------|
| [Logo]  Date Range: [Slicer]  Video: [Slicer]  Day: [Slicer]   |
|---------------------------------------------------------------|
| KPIs:                                                         |
| [Views: 1.2M]  [Subs Gained: 5K]  [Revenue: $2.3K]  [CTR: 3.5%]|
|---------------------------------------------------------------|
| Temporal Trends:                                              |
| [Line Chart: Daily Views]      [Bar Chart: Views by Weekday]   |
| |---------------------|       |---------------------|         |
| | Views ^             |       | Views ^             |         |
| |       |-------------|       |       |-------------|         |
| |       | Date        |       |       | Mon-Sun     |         |
|---------------------------------------------------------------|
| Engagement Insights:                                          |
| [Stacked Bar: Likes, Comments]  [Donut: Subscriber Conversion] |
| |---------------------|       |---------------------|         |
| | Count ^             |       |  Subs/View: 0.5%   |         |
| |       |-------------|       |                     |         |
| |       | Video Title |       |                     |         |
|---------------------------------------------------------------|
| Video Performance Table:                                      |
| | Title | Views | Likes | RPM | Impressions | CTR | Subs/View |
| |-------|-------|-------|-----|-------------|-----|-----------|
| | Vid1  | 100K  | 5K    | 4.5 | 500K        | 3%  | 0.4%      |
| | Vid2  | 80K   | 4K    | 4.0 | 400K        | 2.8%| 0.3%      |
|---------------------------------------------------------------|
| Posting Strategy:                                             |
| [Heatmap: Views by Hour/Day]  [Card: Best Time: Wed 8PM]      |
| |---------------------|       |---------------------|         |
| | Views ^ Mon-Sun     |       | Recommended Posting |         |
| |       |-------------|       | Time                |         |
| |       | 0-23 Hours  |       |                     |         |
+---------------------------------------------------------------+
```

## Detailed Description of Visuals
### Header
- **Title**: "YouTube Video Performance Dashboard"
- **Slicers** (top-right):
  - **Date Range**: Filter by `Video publish time` (e.g., last 30 days, 2024).
  - **Video Title**: Dropdown to select specific videos or all.
  - **Publish Day**: Multi-select for days (Monday–Sunday).
- **Logo**: Optional YouTube or channel logo (top-left).

### Section 1: Key Performance Indicators (KPIs)
- **Visuals**: Five card visuals in a horizontal row.
- **Metrics**:
  - Total Views: `SUM(video_df[Views])` (e.g., "1.2M").
  - Subscribers Gained: `SUM(video_df[Subscribers gained])` (e.g., "5,432").
  - Estimated Revenue: `SUM(video_df[Your estimated revenue (USD)])` (e.g., "$2,345.67").
  - Avg. Click-Through Rate: `AVERAGE(video_df[Impressions click-through rate (%)])` (e.g., "3.45%").
  - Avg. View Duration: `AVERAGE(video_df[Average view duration])` (e.g., "4:32").
- **Styling**: Red text, white background, black borders.
- **Purpose**: Quick overview of channel performance.

### Section 2: Temporal Trends
- **Visuals**:
  - **Line Chart**: Daily views from `Daily_Views_Over_Time.csv`.
    - X-axis: Date.
    - Y-axis: Views.
    - Tooltip: Views and date on hover.
  - **Bar Chart**: Average views by `Publish Day` (from EDA in your notebook).
    - X-axis: Weekday (Monday–Sunday).
    - Y-axis: Average Views.
    - Color: YouTube red.
- **Interactivity**: Click a weekday to filter other visuals; date slicer applies to both.
- **Purpose**: Identify peak viewership days (e.g., Wednesday, as per your EDA).

### Section 3: Engagement Insights
- **Visuals**:
  - **Stacked Bar Chart**: Engagement by video (top 10 by views).
    - X-axis: `Video title`.
    - Y-axis: Count of `Likes`, `Comments added`, `Shares`, `Dislikes`.
    - Colors: Blue (Likes), Green (Comments), Orange (Shares), Red (Dislikes).
  - **Donut Chart**: Subscriber conversion rate.
    - Shows `AVERAGE(video_df[subscribers_per_view])` as a percentage.
    - Inner label: Total `Subscribers gained`.
- **Interactivity**: Filter by video title; drill-down on stacked bar for single-video details.
- **Purpose**: Highlight videos driving engagement and subscriber growth.

### Section 4: Video Performance Table
- **Visual**: Table with sortable columns.
- **Columns**:
  - `Video title`, `Views`, `Likes`, `RPM (USD)`, `Impressions`, `Impressions click-through rate (%)`, `subscribers_per_view`.
- **Interactivity**: Sort by columns (e.g., `Views` descending); click a row to filter visuals.
- **Purpose**: Compare video performance granularly.

### Section 5: Posting Strategy Insights
- **Visuals**:
  - **Heatmap**: Views by `Publish Hour` and `Publish Day`.
    - X-axis: Hour (0–23).
    - Y-axis: Weekday.
    - Color: Red gradient (darker = higher views).
  - **Card**: Recommended posting time.
    - DAX: `MAX(AVERAGE(video_df[Views]))` by `Publish Day` and `Publish Hour` (e.g., "Wednesday, 8 PM").
- **Interactivity**: Hover on heatmap for exact views.
- **Purpose**: Guide creators on optimal posting times, leveraging your feature engineering.

## Implementation in Power BI
1. **Load Data**:
   - Open Power BI Desktop.
   - Get Data > CSV > Import `Aggregated_Metrics_By_Video.csv` and `Daily_Views_Over_Time.csv`.
   - Remove "Total" row in Power Query: Filter `Video` != "Total".
   - Convert `Average view duration` to seconds: `Duration.TotalSeconds([Average view duration])`.
2. **Create Relationships**:
   - Model view > Link `Video publish time` between tables.
3. **Add Visuals**:
   - Cards: Insert > Card > Drag metrics (e.g., `Views`).
   - Line Chart: Insert > Line Chart > Set X-axis to Date, Y-axis to Views.
   - Bar Chart: Insert > Bar Chart > Set X-axis to `Publish Day`, Y-axis to `AVERAGE(Views)`.
   - Stacked Bar: Insert > Stacked Bar Chart > Set X-axis to `Video title`, Values to `Likes`, `Comments added`, etc.
   - Donut Chart: Insert > Donut Chart > Set Values to `subscribers_per_view`.
   - Table: Insert > Table > Add columns.
   - Heatmap: Insert > Matrix > Set Rows to `Publish Day`, Columns to `Publish Hour`, Values to `AVERAGE(Views)`.
   - Recommended Time Card: Insert > Card > Use DAX:
     ```dax
     BestPostingTime = 
     VAR MaxViews = MAXX(
         SUMMARIZE(video_df, video_df[Publish Day], video_df[Publish Hour], "AvgViews", AVERAGE(video_df[Views])),
         [AvgViews]
     )
     VAR BestTime = 
         CALCULATE(
             CONCATENATE(video_df[Publish Day], ", " & video_df[Publish Hour] & " PM"),
             FILTER(
                 SUMMARIZE(video_df, video_df[Publish Day], video_df[Publish Hour], "AvgViews", AVERAGE(video_df[Views])),
                 [AvgViews] = MaxViews
             )
         )
     RETURN BestTime
     ```
4. **Add Slicers**:
   - Insert > Slicer > Add `Video publish time`, `Video title`, `Publish Day`.
   - Format as dropdowns.
5. **Format Dashboard**:
   - View > Themes > Customize > Set colors (red `#FF0000`, white `#FFFFFF`, black `#000000`).
   - Add title text box: "YouTube Video Performance Dashboard".
   - Adjust font (Roboto, size 12–14) and borders.
6. **Save and Export**:
   - File > Save As > `YouTube_Dashboard.pbix`.
   - File > Export > Export to PDF or take a screenshot for an image.

## How to Get a Sample Image
1. **Build in Power BI Desktop**:
   - Follow the implementation steps above.
   - After creating the dashboard, take a screenshot (Windows: `Win + PrtSc`) or export to PDF and extract the page.
   - Save as `YouTube_Dashboard.png` or `YouTube_Dashboard.jpg`.
2. **Use Online Templates** (as per Windsor.ai):[](https://windsor.ai/power-bi-youtube-dashboard/)
   - Visit [Windsor.ai](https://windsor.ai/power-bi-youtube-analytics-dashboard/) for a free Power BI YouTube Analytics template.
   - Download the `.pbix` file, connect your dataset, and customize visuals to match your metrics (e.g., add `subscribers_per_view`).
   - Take a screenshot of the rendered dashboard.
3. **Coupler.io Templates** (as per Coupler.io):[](https://blog.coupler.io/youtube-analytics-to-power-bi/)
   - Check [Coupler.io’s Power BI templates](https://blog.coupler.io/youtube-analytics-power-bi/) for YouTube Analytics.
   - Request their Power BI version of the YouTube dashboard (originally in Looker Studio) and adapt it to your data.
   - Capture the dashboard image.
4. **GitHub Resources**:
   - Explore [KammampatiSaivamshi’s YouTube-Video-Performance-Predictor-Audience-Insights-System](https://github.com/prateekralhan/Youtube-Data-Analytics-using-PowerBI).[](https://github.com/prateekralhan/Youtube-Data-Analytics-using-PowerBI)
   - Download the `.pbix` file, import your CSV, and generate a screenshot.
5. **Mockup Tools**:
   - Use tools like Figma or Canva to create a mockup image based on the ASCII layout and description.
   - Import the ASCII layout into Canva, add shapes for visuals, and color with YouTube’s palette.
   - Export as `YouTube_Dashboard_Mockup.png`.

## Example Insights
- **Top Videos**: Table identifies videos with high `Views` and `subscribers_per_view` (e.g., "Vid1: 100K views, 0.4% conversion").
- **Optimal Posting**: Heatmap and card suggest posting on Wednesday at 8 PM, based on your `Publish Day` analysis.
- **Engagement**: Stacked bar shows videos with high `Comments added`, indicating discussion-driven content.
- **Revenue**: KPI card highlights `RPM (USD)` and total revenue, guiding monetization strategies.

## Notes
- **Assumptions**: The "Total" row is removed, and `Average view duration` is in seconds for numerical analysis.
- **Customization**: Add visuals (e.g., audience demographics) if more data is available.
- **Security**: Ensure data privacy when sharing `.pbix` files, as noted by Windsor.ai.[](https://windsor.ai/power-bi-youtube-dashboard/)
- **Inspiration**: Adapted from Windsor.ai’s YouTube Analytics template and Coupler.io’s bar chart examples for views and engagement.[](https://windsor.ai/power-bi-youtube-dashboard/)[](https://blog.coupler.io/youtube-analytics-to-power-bi/)

This mockup provides a blueprint to create a Power BI dashboard image that aligns with your project’s goals, enabling data-driven decisions for YouTube content creators.