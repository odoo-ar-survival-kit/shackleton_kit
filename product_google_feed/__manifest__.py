# -*- coding: utf-8 -*-

{
    'name': 'Google merchand product feed',
    'version': '0.1',
    'category': 'website',
    'description': """
Google merchand product feed
======================
Google Merchant Center lets millions of online shoppers discover, explore, and buy your products.
A suite of programs, including Shopping ads, surfaces across Google, and Shopping Actions,
offer different ways for you to get the right products to the right customers. Before you begin

You’ll need a Google Account (like Gmail) to sign up for Merchant Center. If you don't have a Google account, go to accounts.google.com and click Create account.

When you’re ready, go to merchants.google.com and sign in with your Google Account to get started.
Enter your business information

Your business information will be used in each program you sign up for. You’ll only have to
enter this information once. Add the country where your business is registered as the “Business country.”

Your business display name can be your business’s name, your website’s name, or your store
name. Remember: The name you enter as your business display name will be used as your Merchant Center account name, and users will see this name across Google.    """,
    'author': 'Filoquin',
    'website': 'http://www.sipecu.com.ar',
    'depends': ['website_sale', 'stock'],
    'installable': True,
    'data': [
        'views/product_google_feed.xml',
        'data/product_google_producttype.xml',
        'security/ir.model.access.csv',
    ],
    'images': [],
    'auto_install': False,
}
