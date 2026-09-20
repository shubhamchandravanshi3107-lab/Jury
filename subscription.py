# JURY - Personal Subscription Spend Auditor
# Beginner Python version for Hackathon Problem 11(OPEN INNOVATION)
# Uses only basic W3Schools Python topics.

import datetime

print("==" * 29)
print("        JURY - SUBSCRIPTION SPEND AUDITOR")
print("==" * 29)
print("Add your monthly subscriptions to check your spending.\n")

# Lists and dictionaries keep every subscription together.
subscriptions = []
#services categories
categories = ["Streaming", "Music", "Gaming", "Fitness", "Cloud Storage",
              "News", "Education", "Other"]

# Ask for the number of subscriptions.
valid_count = False
while valid_count == False:
    try:
        number_of_subscriptions = int(input("How many subscriptions do you have? "))
        if number_of_subscriptions >= 0:
            valid_count = True
        else:
            print("Please enter 0 or a positive number.")
    except ValueError:
        print("Please enter a whole number.")

# Get subscription details.
for number in range(number_of_subscriptions):
    print("\nSubscription", number + 1)
    service_name = input("Service name: ").strip()

    while service_name == "":
        print("The service name cannot be empty.")
        service_name = input("Service name: ").strip()

    print("Categories:", ", ".join(categories))
    service_category = input("Category: ").title().strip()
    if service_category not in categories:
        service_category = "Other"

    valid_cost = False
    while valid_cost == False:
        try:
            monthly_cost = float(input("Monthly cost (Rs.): "))
            if monthly_cost >= 0:
                valid_cost = True
            else:
                print("Cost cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")

    subscription = {"name": service_name, "category": service_category,
                    "cost": monthly_cost}
    subscriptions.append(subscription)

# Find the total monthly spend.
monthly_total = 0
for subscription in subscriptions:
    monthly_total = monthly_total + subscription["cost"]

print("\nYour total monthly subscription spend is Rs. {:.2f}".format(monthly_total))

# Compare total spend with the user's budget.
valid_budget = False
while valid_budget == False:
    try:
        monthly_budget = float(input("Enter your monthly subscription budget (Rs.): "))
        if monthly_budget >= 0:
            valid_budget = True
        else:
            print("Budget cannot be negative.")
    except ValueError:
        print("Please enter a valid number.")

budget_difference = monthly_budget - monthly_total
print("\nBUDGET CHECK")
if budget_difference >= 0:
    print("You are within budget by Rs. {:.2f}".format(budget_difference))
else:
    over_budget = budget_difference * -1
    print("You are over budget by Rs. {:.2f}".format(over_budget))

# Copy and rank subscriptions from most expensive to least expensive.
ranked_subscriptions = []
for subscription in subscriptions:
    ranked_subscriptions.append(subscription)

for first_number in range(len(ranked_subscriptions)):
    for second_number in range(first_number + 1, len(ranked_subscriptions)):
        if ranked_subscriptions[first_number]["cost"] < ranked_subscriptions[second_number]["cost"]:
            temporary_subscription = ranked_subscriptions[first_number]
            ranked_subscriptions[first_number] = ranked_subscriptions[second_number]
            ranked_subscriptions[second_number] = temporary_subscription

print("\nCOST RANKING")
if len(ranked_subscriptions) == 0:
    print("No subscriptions were added.")
else:
    for subscription in ranked_subscriptions:
        print("- {} ({}) - Rs. {:.2f}/month".format(
            subscription["name"], subscription["category"], subscription["cost"]))

# Check for multiple subscriptions in the same category.
checked_categories = []
possible_saving = 0
overlap_found = False
print("\nDUPLICATE / OVERLAP CHECK")

for subscription in subscriptions:
    category = subscription["category"]
    if category not in checked_categories and category != "Other":
        checked_categories.append(category)
        same_category = []

        for item in subscriptions:
            if item["category"] == category:
                same_category.append(item)

        if len(same_category) > 1:
            overlap_found = True
            cheapest_subscription = same_category[0]
            category_total = 0
            print("You have", len(same_category), category, "subscriptions:")

            for item in same_category:
                print("  - {}: Rs. {:.2f}".format(item["name"], item["cost"]))
                category_total = category_total + item["cost"]
                if item["cost"] < cheapest_subscription["cost"]:
                    cheapest_subscription = item

            category_saving = category_total - cheapest_subscription["cost"]
            possible_saving = possible_saving + category_saving
            print("  Suggestion: review these plans. Keep {} only if it meets your needs.".format(
                cheapest_subscription["name"]))
            print("  Possible saving: Rs. {:.2f}/month\n".format(category_saving))

if overlap_found == False:
    print("No category overlaps found.")

# Show the next 12 months of subscription spending.
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
current_month = datetime.datetime.now().month - 1
running_total = 0

print("\nNEXT 12 MONTHS")
for number in range(12):
    month_number = (current_month + number) % 12
    running_total = running_total + monthly_total
    print("{} - Rs. {:.2f} cumulative".format(months[month_number], running_total))

print("\n" + "=" * 55)
print("AUDIT SUMMARY")
print("=" * 55)
print("Active subscriptions:", len(subscriptions))
print("Monthly spend: Rs. {:.2f}".format(monthly_total))
print("12-month spend: Rs. {:.2f}".format(running_total))
print("Possible monthly saving after review: Rs. {:.2f}".format(possible_saving))
print("Thank you for using JURY!")