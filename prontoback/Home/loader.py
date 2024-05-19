import pandas as pd
from models import MenuItem, Category

df = pd.read_excel('./food menu.xlsx')
df.rename(columns={'Section': 'Category'}, inplace=True)

for _, row in df.iterrows():
    # Get or create the Category
    category, _ = Category.objects.get_or_create(name=row['Category'])  

    MenuItem.objects.create(
        name=row['Item'],
        description=row.get('Description', ''),  
        price=row.get('Price', 0.00),
        category=category
    )
