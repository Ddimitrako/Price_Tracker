# Price_Tracker
This project was inspired and implemented after my failure to buy my dream car 
after i found it in sale for half of its price but over 200 people have viewed the ad and someone bought it immediately.

Let me explain how this project works:

In this python project we request data from the car.gr server
and then we parse them with the beautifulSoup4 to 
find prices and links for every car that exist in the current 
page*. Then the system check if these cars meets specific criteria that every customer has requested from us.
If they meet the criteria system sent an email to the given email of the customer. The sented email contains the price of the car which is in the range of their value that they can afford but also the link of the car so they can navigate to the main webpage.

Also the user set the frequency that the system scan the webpage.
System also keep data logs from all the searches.

*The customer give me the link of the car he wants to track.
This link is the link in the broswer after the he presses the result button.
Customer can and is recomented to add criteria to his search before he sent us the link.

# Some example photos 
![](images/main.jpg)
![](images/main2.jpg) 
