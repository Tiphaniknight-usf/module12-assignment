# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
np.random.seed(42)

stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}
store_df = pd.DataFrame(store_data)

departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

store_performance = {
    "Tampa": 1.0, "Orlando": 0.85, "Miami": 1.2,
    "Jacksonville": 0.75, "Gainesville": 0.65
}

dept_performance = {
    "Produce": 1.2, "Dairy": 1.0, "Bakery": 0.85,
    "Grocery": 0.95, "Prepared Foods": 1.1
}

for date in dates:
    month = date.month
    seasonal_factor = 1.15 if month in [6,7,8] else 1.25 if month==12 else 0.9 if month in [1,2] else 1
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0

    for store in stores:
        for dept in departments:
            for category in categories[dept]:
                base_sales = np.random.normal(500,100)
                sales_amount = base_sales * store_performance[store] * dept_performance[dept] * seasonal_factor * dow_factor
                sales_amount *= np.random.normal(1.0,0.1)

                base_margin = {
                    "Produce":0.25,"Dairy":0.22,"Bakery":0.35,
                    "Grocery":0.20,"Prepared Foods":0.40
                }[dept]

                profit_margin = base_margin * np.random.normal(1.0,0.05)
                profit_margin = max(min(profit_margin,0.5),0.15)
                profit = sales_amount * profit_margin

                sales_data.append({
                    "Date":date,
                    "Store":store,
                    "Department":dept,
                    "Category":category,
                    "Sales":round(sales_amount,2),
                    "ProfitMargin":round(profit_margin,4),
                    "Profit":round(profit,2)
                })

sales_df = pd.DataFrame(sales_data)

# Customer data
customer_data=[]
segments=["Health Enthusiast","Gourmet Cook","Family Shopper","Budget Organic","Occasional Visitor"]
segment_probs=[0.25,0.20,0.30,0.15,0.10]
store_probs={"Tampa":0.25,"Orlando":0.20,"Miami":0.30,"Jacksonville":0.15,"Gainesville":0.10}

for i in range(5000):
    age=max(min(int(np.random.normal(42,15)),85),18)
    gender=np.random.choice(["M","F"],p=[0.48,0.52])
    income=max(int(np.random.normal(85,30)),20)*1000
    segment=np.random.choice(segments,p=segment_probs)
    preferred_store=np.random.choice(stores,p=list(store_probs.values()))

    if segment=="Health Enthusiast":
        visits, basket=np.random.randint(8,15), np.random.normal(75,15)
    elif segment=="Gourmet Cook":
        visits, basket=np.random.randint(4,10), np.random.normal(120,25)
    elif segment=="Family Shopper":
        visits, basket=np.random.randint(5,12), np.random.normal(150,30)
    elif segment=="Budget Organic":
        visits, basket=np.random.randint(6,10), np.random.normal(60,10)
    else:
        visits, basket=np.random.randint(1,5), np.random.normal(45,15)

    visits=max(min(visits,30),1)
    basket=max(basket,15)
    monthly=visits*basket

    tier="Platinum" if monthly>1000 else "Gold" if monthly>500 else "Silver" if monthly>200 else "Bronze"

    customer_data.append({
        "CustomerID":f"C{i+1:04d}",
        "Age":age,
        "Gender":gender,
        "Income":income,
        "Segment":segment,
        "PreferredStore":preferred_store,
        "VisitsPerMonth":visits,
        "AvgBasketSize":round(basket,2),
        "MonthlySpend":round(monthly,2),
        "LoyaltyTier":tier
    })

customer_df=pd.DataFrame(customer_data)

# Operational data
operational_data=[]
for store in stores:
    row=store_df[store_df["Store"]==store].iloc[0]
    sales=sales_df[sales_df["Store"]==store]["Sales"].sum()
    profit=sales_df[sales_df["Store"]==store]["Profit"].sum()

    operational_data.append({
        "Store":store,
        "AnnualSales":round(sales,2),
        "AnnualProfit":round(profit,2),
        "SalesPerSqFt":round(sales/row["SquareFootage"],2),
        "SalesPerStaff":round(sales/row["StaffCount"],2)
    })

operational_df=pd.DataFrame(operational_data)

# ---------------- ANALYSIS FUNCTIONS ----------------

def analyze_sales_performance():
    return {
        "total_sales": float(sales_df["Sales"].sum()),
        "total_profit": float(sales_df["Profit"].sum()),
        "avg_profit_margin": float(sales_df["ProfitMargin"].mean()),
        "sales_by_store": sales_df.groupby("Store")["Sales"].sum(),
        "sales_by_dept": sales_df.groupby("Department")["Sales"].sum()
    }

def visualize_sales_distribution():
    fig1, ax1 = plt.subplots()
    sales_df.groupby("Store")["Sales"].sum().plot(kind="bar", ax=ax1)

    fig2, ax2 = plt.subplots()
    sales_df.groupby("Department")["Sales"].sum().plot(kind="bar", ax=ax2)

    fig3, ax3 = plt.subplots()
    sales_df.groupby("Date")["Sales"].sum().plot(ax=ax3)

    return fig1, fig2, fig3

def analyze_customer_segments():
    return {
        "segment_counts": customer_df["Segment"].value_counts(),
        "segment_avg_spend": customer_df.groupby("Segment")["MonthlySpend"].mean(),
        "segment_loyalty": pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])
    }

def analyze_sales_correlations():
    merged=pd.merge(operational_df,store_df,on="Store")
    corr=merged.corr(numeric_only=True)

    fig, ax = plt.subplots()
    ax.imshow(corr)

    return {
        "store_correlations": corr,
        "top_correlations": list(corr["AnnualSales"].items()),
        "correlation_fig": fig
    }

def compare_store_performance():
    fig, ax = plt.subplots()
    operational_df.plot(x="Store", y=["SalesPerSqFt","SalesPerStaff"], kind="bar", ax=ax)

    return {
        "efficiency_metrics": operational_df[["Store","SalesPerSqFt","SalesPerStaff"]],
        "performance_ranking": operational_df.set_index("Store")["AnnualProfit"].rank(ascending=False),
        "comparison_fig": fig
    }

def analyze_seasonal_patterns():
    sales_df["Month"]=sales_df["Date"].dt.month
    monthly=sales_df.groupby("Month")["Sales"].sum()

    fig, ax = plt.subplots()
    monthly.plot(ax=ax)

    return {
        "monthly_sales": monthly,
        "dow_sales": sales_df.groupby(sales_df["Date"].dt.day_name())["Sales"].sum(),
        "seasonal_fig": fig
    }

def predict_store_sales():
    merged=pd.merge(operational_df,store_df,on="Store")
    features=["SquareFootage","StaffCount","WeeklyMarketingSpend","YearsOpen"]

    X=merged[features].values
    y=merged["AnnualSales"].values

    X=np.column_stack((np.ones(len(X)),X))
    beta=np.linalg.inv(X.T@X)@X.T@y

    coef=dict(zip(["Intercept"]+features,beta))

    fig, ax = plt.subplots()
    ax.scatter(y, X@beta)

    return {
        "coefficients": coef,
        "r_squared": float(1 - np.sum((y-X@beta)**2)/np.sum((y-y.mean())**2)),
        "predictions": pd.Series(X@beta,index=merged["Store"]),
        "model_fig": fig
    }

def forecast_department_sales():
    trends=sales_df.groupby(["Date","Department"])["Sales"].sum().unstack()

    fig, ax = plt.subplots()
    trends.plot(ax=ax)

    return {
        "dept_trends": trends,
        "growth_rates": trends.pct_change().mean(),
        "forecast_fig": fig
    }

def identify_profit_opportunities():
    combo=sales_df.groupby(["Store","Department"])["Profit"].sum().reset_index()

    return {
        "top_combinations": combo.sort_values("Profit",ascending=False).head(10),
        "underperforming": combo.sort_values("Profit").head(10),
        "opportunity_score": combo.groupby("Store")["Profit"].sum()
    }

def develop_recommendations():
    return [
        "Invest more in Miami and Tampa.",
        "Focus on Produce and Prepared Foods.",
        "Improve efficiency in Gainesville.",
        "Target high-value customers.",
        "Optimize staffing levels."
    ]

def generate_executive_summary():
    print("\nOVERVIEW")
    print("GreenGrocer shows strong store and seasonal performance trends.")

    print("\nKEY FINDINGS")
    print("- Miami leads in sales")
    print("- Produce and Prepared Foods are most profitable")
    print("- Seasonal peaks occur in summer and December")

    print("\nRECOMMENDATIONS")
    print("- Invest in top stores")
    print("- Focus on high-margin departments")
    print("- Improve low-performing stores")

    print("\nEXPECTED IMPACT")
    print("Improved profitability and efficiency across stores.")

def main():
    analyze_sales_performance()
    visualize_sales_distribution()
    analyze_customer_segments()
    analyze_sales_correlations()
    compare_store_performance()
    analyze_seasonal_patterns()
    predict_store_sales()
    forecast_department_sales()
    identify_profit_opportunities()
    develop_recommendations()
    generate_executive_summary()
    plt.show()

if __name__=="__main__":
    main()