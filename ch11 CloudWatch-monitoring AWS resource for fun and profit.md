# CloudWatch: monitoring AWS resources for fun and profit
## 11.1 AWS Budgets
### 11.1.1 Creating a budget
In this section, you’ll create an AWS budget and set it to issue email
alerts if your monthly usage charges exceed a specified limit. To start
the process, follow these steps (see figure 11.1):
1. Give your budget a name.
2. Select Cost if, as in this case, your goal is to keep an eye on your
account costs. Or select Usage if you’re interested in tracking
account activity by the number of service units consumed rather
than cost—perhaps to see whether your current deployment profile requires a reset.
3. Set the budget period. This is the time period—monthly, quarterly, or yearly—you’d like to use to measure costs; any budget
amount you select in step 5 will be applied in relation to the time
period you set here.
4. Set the start and end dates between which this budget will remain
active.
5. Set Budgeted Amount to the maximum you’re willing to spend
during each selected period before an alert is triggered.