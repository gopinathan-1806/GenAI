# RTCFR Framework Example

We need to provide proper prompt to get the better response. To provide the better prompt, use the below framework.

## Prompt

### Role
You are a **master chef and nutrition planner** for a college cafeteria.

### Task
Create a **15-day protein-rich meal plan** for students, including breakfast, lunch, evening snacks, and dinner. Ensure that no food item is repeated during the 15 days.

### Context
- Students are **South Indian male students** aged **15-18 years**.
- Meals should be nutritious, balanced, and protein-focused.
- Include both **vegetarian** and **non-vegetarian** options.
- Evening snacks must be included.

### Few-Shot
Example meal combinations:
- Ragi Dosa + Sambar + Boiled Eggs
- Sprouts Chaat
- Paneer Rice Bowl
- Grilled Chicken with Millet Rice

### Response / Result
Return the output in a **tabular format** with the following columns:

```text
Date | Day | Time | Menu Name | Nutrition Content | Calories | Veg/Non-Veg
```

The meal plan should cover all 15 days and include calorie and nutrition information for each meal.

<img width="930" height="696" alt="Screenshot 2026-08-29 at 10 23 08 PM" src="https://github.com/user-attachments/assets/31379635-e0fa-4bd3-9eee-998b18ae68bc" />
