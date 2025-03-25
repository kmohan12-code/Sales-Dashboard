
Superstore EDA Dashboard  

An interactive **Exploratory Data Analysis (EDA) dashboard** built using **Streamlit** and **Plotly** to analyze and visualize sales data from a Superstore dataset.  

Features  

-  File Upload:** Upload CSV, TXT, XLSX, or XLS files for analysis.  
-  Date Filtering:** Select a custom date range for analysis.  
-  Region, State & City Filtering:** Drill down into sales data by location.  
-  Visualizations:**  
  - **Category-wise Sales** (Bar Chart)  
  - **Region-wise Sales** (Pie Chart)  
  - **Hierarchical Sales View** (Treemap)  
  - **Sales vs. Profit** (Scatter Plot)  
  - **Segment-wise & Category-wise Sales** (Pie Charts)  
  - **Month-wise Sub-Category Sales** (Table Summary)  

##  How to Run  

   
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  

3. **Run the Application**  
   ```bash
   streamlit run app.py
   ```  

## Dataset  

The dashboard is designed to work with **Superstore Sales Data** containing columns like:  
- **Order Date**  
- **Sales**  
- **Profit**  
- **Region, State, City**  
- **Category, Sub-Category**  
- **Quantity**  


## Future Improvements  

- Add more advanced **machine learning insights** (e.g., sales forecasting).  
- Enable **real-time data updates** from external sources.  
- Improve **UI/UX** for a better experience.
  
