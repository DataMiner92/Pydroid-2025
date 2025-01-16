import tkinter as tk
from tkinter.font import Font 


kenya_counties = {
    "Mombasa": {
        "Population": "1,208,333",
        "Area": "229.7 km²",
        "Governor": "Abdulswamad Nassir",
        "Literacy Level": "78%",
        "Annual Revenue": "KES 7.2 billion",
        "Annual Budget Allocation": "KES 9.5 billion",
        "Number of Constituencies": 6,
        "Region": "Coast",
        "Persons with Disability": "15,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "Kwale": {
        "Population": "866,820",
        "Area": "8,270.2 km²",
        "Governor": "Fátuma Achani",
        "Literacy Level": "65%",
        "Annual Revenue": "KES 4.5 billion",
        "Annual Budget Allocation": "KES 5.8 billion",
        "Number of Constituencies": 4,
        "Region": "Coast",
        "Persons with Disability": "12,000",
        "Uwezo Fund Disbursement": "KES 40 million"
    },
    "Kilifi": {
        "Population": "1,453,787",
        "Area": "12,245.9 km²",
        "Governor": "Gideon Mung'aro",
        "Literacy Level": "70%",
        "Annual Revenue": "KES 5.1 billion",
        "Annual Budget Allocation": "KES 6.7 billion",
        "Number of Constituencies": 7,
        "Region": "Coast",
        "Persons with Disability": "18,000",
        "Uwezo Fund Disbursement": "KES 60 million"
    },
    "Tana River": {
        "Population": "315,943",
        "Area": "35,375.8 km²",
        "Governor": "Dhadho Godhana",
        "Literacy Level": "57%",
        "Annual Revenue": "KES 3.0 billion",
        "Annual Budget Allocation": "KES 3.9 billion",
        "Number of Constituencies": 3,
        "Region": "Coast",
        "Persons with Disability": "10,000",
        "Uwezo Fund Disbursement": "KES 35 million"
    },
    "Lamu": {
        "Population": "143,920",
        "Area": "6,474.7 km²",
        "Governor": "Issa Abdallah Timamy",
        "Literacy Level": "63%",
        "Annual Revenue": "KES 1.6 billion",
        "Annual Budget Allocation": "KES 2.1 billion",
        "Number of Constituencies": 2,
        "Region": "Coast",
        "Persons with Disability": "8,000",
        "Uwezo Fund Disbursement": "KES 25 million"
    },
    "Taita-Taveta": {
        "Population": "340,671",
        "Area": "17,083.9 km²",
        "Governor": "Andréw Mwadime",
        "Literacy Level": "68%",
        "Annual Revenue": "KES 3.5 billion",
        "Annual Budget Allocation": "KES 4.8 billion",
        "Number of Constituencies": 4,
        "Region": "Coast",
        "Persons with Disability": "11,000",
        "Uwezo Fund Disbursement": "KES 45 million"
    },
    "Garissa": {
        "Population": "841,353",
        "Area": "45,720.2 km²",
        "Governor": "Nadhif Jama",
        "Literacy Level": "54%",
        "Annual Revenue": "KES 4.3 billion",
        "Annual Budget Allocation": "KES 5.6 billion",
        "Number of Constituencies": 6,
        "Region": "North Eastern",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 55 million"
    },
    "Wajir": {
        "Population": "781,263",
        "Area": "56,685.8 km²",
        "Governor": "Ahmed Abdullahi",
        "Literacy Level": "50%",
        "Annual Revenue": "KES 4.0 billion",
        "Annual Budget Allocation": "KES 5.3 billion",
        "Number of Constituencies": 8,
        "Region": "North Eastern",
        "Persons with Disability": "13,000",
        "Uwezo Fund Disbursement": "KES 48 million"
    },
    "Mandera": {
        "Population": "867,457",
        "Area": "25,797.7 km²",
        "Governor": "Mohamed Adán Khalif",
        "Literacy Level": "49%",
        "Annual Revenue": "KES 3.8 billion",
        "Annual Budget Allocation": "KES 4.9 billion",
        "Number of Constituencies": 8,
        "Region": "North Eastern",
        "Persons with Disability": "17,000",
        "Uwezo Fund Disbursement": "KES 60 million"
    },
    "Marsabit": {
        "Population": "459,785",
        "Area": "66,923.1 km²",
        "Governor": "Mohamud Ali",
        "Literacy Level": "45%",
        "Annual Revenue": "KES 3.2 billion",
        "Annual Budget Allocation": "KES 4.5 billion",
        "Number of Constituencies": 6,
        "Region": "Eastern",
        "Persons with Disability": "12,000",
        "Uwezo Fund Disbursement": "KES 45 million"
    },
    "Isiolo": {
        "Population": "268,002",
        "Area": "25,336.1 km²",
        "Governor": "Abdi Hassan Guyo",
        "Literacy Level": "52%",
        "Annual Revenue": "KES 2.8 billion",
        "Annual Budget Allocation": "KES 3.6 billion",
        "Number of Constituencies": 3,
        "Region": "Eastern",
        "Persons with Disability": "9,000",
        "Uwezo Fund Disbursement": "KES 30 million"
    },
    "Meru": {
        "Population": "1,545,714",
        "Area": "6,936.2 km²",
        "Governor": "Kawira Mwangaza",
        "Literacy Level": "72%",
        "Annual Revenue": "KES 6.1 billion",
        "Annual Budget Allocation": "KES 8.0 billion",
        "Number of Constituencies": 8,
        "Region": "Eastern",
        "Persons with Disability": "20,000",
        "Uwezo Fund Disbursement": "KES 70 million"
    },
    "Tharaka-Nithi": {
        "Population": "393,177",
        "Area": "2,409.5 km²",
        "Governor": "Muthomi Njuki",
        "Literacy Level": "67%",
        "Annual Revenue": "KES 3.3 billion",
        "Annual Budget Allocation": "KES 4.2 billion",
        "Number of Constituencies": 3,
        "Region": "Eastern",
        "Persons with Disability": "10,000",
        "Uwezo Fund Disbursement": "KES 35 million"
    },
    "Embu": {
        "Population": "608,599",
        "Area": "2,818.9 km²",
        "Governor": "Cecily Mbarire",
        "Literacy Level": "70%",
        "Annual Revenue": "KES 3.7 billion",
        "Annual Budget Allocation": "KES 4.8 billion",
        "Number of Constituencies": 4,
        "Region": "Eastern",
        "Persons with Disability": "11,000",
        "Uwezo Fund Disbursement": "KES 40 million"
    },
    "Kitui": {
        "Population": "1,136,187",
        "Area": "30,430.2 km²",
        "Governor": "Julius Malombe",
        "Literacy Level": "63%",
        "Annual Revenue": "KES 5.0 billion",
        "Annual Budget Allocation": "KES 6.3 billion",
        "Number of Constituencies": 8,
        "Region": "Eastern",
        "Persons with Disability": "18,000",
        "Uwezo Fund Disbursement": "KES 55 million"
    },
    "Machakos": {
        "Population": "1,421,932",
        "Area": "6,208.3 km²",
        "Governor": "Wavinya Ndeti",
        "Literacy Level": "68%",
        "Annual Revenue": "KES 6.3 billion",
        "Annual Budget Allocation": "KES 7.9 billion",
        "Number of Constituencies": 8,
        "Region": "Eastern",
        "Persons with Disability": "20,000",
        "Uwezo Fund Disbursement": "KES 75 million"
    },
    "Makueni": {
        "Population": "987,653",
        "Area": "8,008.9 km²",
        "Governor": "Mutula Kilonzo",
        "Literacy Level": "65%",
        "Annual Revenue": "KES 4.8 billion",
        "Annual Budget Allocation": "KES 6.1 billion",
        "Number of Constituencies": 5,
        "Region": "Eastern",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "Nyandarua": {
        "Population": "638,289",
        "Area": "3,107.7 km²",
        "Governor": "Badilisha Kiarie",
        "Literacy Level": "73%",
        "Annual Revenue": "KES 3.9 billion",
        "Annual Budget Allocation": "KES 5.2 billion",
        "Number of Constituencies": 5,
        "Region": "Central",
        "Persons with Disability": "11,000",
        "Uwezo Fund Disbursement": "KES 40 million"
    },
    "Nyeri": {
        "Population": "759,164",
        "Area": "3,356.9 km²",
        "Governor": "Mutahi Kahiga",
        "Literacy Level": "74%",
        "Annual Revenue": "KES 4.2 billion",
        "Annual Budget Allocation": "KES 5.8 billion",
        "Number of Constituencies": 6,
        "Region": "Central",
        "Persons with Disability": "13,000",
        "Uwezo Fund Disbursement": "KES 45 million"
    },
    "Kirinyaga": {
        "Population": "610,411",
        "Area": "1,205.4 km²",
        "Governor": "Anne Waiguru",
        "Literacy Level": "71%",
        "Annual Revenue": "KES 4.0 billion",
        "Annual Budget Allocation": "KES 5.4 billion",
        "Number of Constituencies": 4,
        "Region": "Central",
        "Persons with Disability": "10,000",
        "Uwezo Fund Disbursement": "KES 35 million"
    },
    "Murang'a": {
        "Population": "1,056,640",
        "Area": "2,325.8 km²",
        "Governor": "Irungu Kang'ata",
        "Literacy Level": "69%",
        "Annual Revenue": "KES 5.5 billion",
        "Annual Budget Allocation": "KES 7.1 billion",
        "Number of Constituencies": 5,
        "Region": "Central",
        "Persons with Disability": "17,000",
        "Uwezo Fund Disbursement": "KES 65 million"
    },
    "Kiambu": {
        "Population": "2,417,735",
        "Area": "2,449.2 km²",
        "Governor": "Kimani Wa Matangi",
        "Literacy Level": "79%",
        "Annual Revenue": "KES 9.8 billion",
        "Annual Budget Allocation": "KES 12.4 billion",
        "Number of Constituencies": 12,
        "Region": "Central",
        "Persons with Disability": "25,000",
        "Uwezo Fund Disbursement": "KES 100 million"
    },
    "Turkana": {
        "Population": "926,976",
        "Area": "68,680.3 km²",
        "Governor": "Jeremiah Lomurkai",
        "Literacy Level": "42%",
        "Annual Revenue": "KES 3.5 billion",
        "Annual Budget Allocation": "KES 4.7 billion",
        "Number of Constituencies": 7,
        "Region": "Rift Valley",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "West Pokot": {
        "Population": "621,241",
        "Area": "8,418.2 km²",
        "Governor": "Simón Kachapin",
        "Literacy Level": "55%",
        "Annual Revenue": "KES 2.7 billion",
        "Annual Budget Allocation": "KES 3.5 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "10,000",
        "Uwezo Fund Disbursement": "KES 30 million"
    },
    "Samburu": {
        "Population": "310,327",
        "Area": "20,182.5 km²",
        "Governor": "Jonathan Lati Leleliit",
        "Literacy Level": "46%",
        "Annual Revenue": "KES 2.1 billion",
        "Annual Budget Allocation": "KES 2.8 billion",
        "Number of Constituencies": 3,
        "Region": "Rift Valley",
        "Persons with Disability": "8,000",
        "Uwezo Fund Disbursement": "KES 25 million"
    },
    "Trans-Nzoia": {
        "Population": "990,341",
        "Area": "2,495.5 km²",
        "Governor": "George Natembeya",
        "Literacy Level": "60%",
        "Annual Revenue": "KES 4.0 billion",
        "Annual Budget Allocation": "KES 5.2 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "Uasin Gishu": {
        "Population": "1,163,186",
        "Area": "3,345.2 km²",
        "Governor": "Jonathan Bii",
        "Literacy Level": "66%",
        "Annual Revenue": "KES 5.3 billion",
        "Annual Budget Allocation": "KES 7.0 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "18,000",
        "Uwezo Fund Disbursement": "KES 65 million"
    },
    "Elgeyo-Marakwet": {
        "Population": "454,480",
        "Area": "3,049.7 km²",
        "Governor": "Wisley Rotich",
        "Literacy Level": "58%",
        "Annual Revenue": "KES 2.6 billion",
        "Annual Budget Allocation": "KES 3.4 billion",
        "Number of Constituencies": 4,
        "Region": "Rift Valley",
        "Persons with Disability": "11,000",
        "Uwezo Fund Disbursement": "KES 40 million"
    },
    "Nandi": {
        "Population": "885,711",
        "Area": "2,884.7 km²",
        "Governor": "Stephen Sang",
        "Literacy Level": "64%",
        "Annual Revenue": "KES 4.1 billion",
        "Annual Budget Allocation": "KES 5.3 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "Baringo": {
        "Population": "666,763",
        "Area": "11,075.3 km²",
        "Governor": "Benjamin Chemboi",
        "Literacy Level": "53%",
        "Annual Revenue": "KES 3.2 billion",
        "Annual Budget Allocation": "KES 4.3 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "12,000",
        "Uwezo Fund Disbursement": "KES 45 million"
    },
    "Laikipia": {
        "Population": "518,560",
        "Area": "9,462.2 km²",
        "Governor": "Joshua Irungu",
        "Literacy Level": "70%",
        "Annual Revenue": "KES 4.3 billion",
        "Annual Budget Allocation": "KES 5.5 billion",
        "Number of Constituencies": 5,
        "Region": "Rift Valley",
        "Persons with Disability": "10,000",
        "Uwezo Fund Disbursement": "KES 35 million"
    },
    "Nakuru": {
        "Population": "2,283,595",
        "Area": "7,495.1 km²",
        "Governor": "Susan Kihika",
        "Literacy Level": "75%",
        "Annual Revenue": "KES 7.8 billion",
        "Annual Budget Allocation": "KES 10.2 billion",
        "Number of Constituencies": 11,
        "Region": "Rift Valley",
        "Persons with Disability": "23,000",
        "Uwezo Fund Disbursement": "KES 90 million"
    },
    "Narok": {
        "Population": "1,157,873",
        "Area": "17,921.2 km²",
        "Governor": "Samuel Tunai",
        "Literacy Level": "57%",
        "Annual Revenue": "KES 6.2 billion",
        "Annual Budget Allocation": "KES 8.0 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "15,000",
        "Uwezo Fund Disbursement": "KES 60 million"
    },
    "Kajiado": {
        "Population": "1,117,840",
        "Area": "21,292.7 km²",
        "Governor": "Joseph Ole Lenku",
        "Literacy Level": "63%",
        "Annual Revenue": "KES 5.5 billion",
        "Annual Budget Allocation": "KES 7.3 billion",
        "Number of Constituencies": 6,
        "Region": "Rift Valley",
        "Persons with Disability": "17,000",
        "Uwezo Fund Disbursement": "KES 65 million"
    },
    "Kericho": {
        "Population": "901,777",
        "Area": "2,479.0 km²",
        "Governor": "Susan Kikwai",
        "Literacy Level": "66%",
        "Annual Revenue": "KES 4.0 billion",
        "Annual Budget Allocation": "KES 5.3 billion",
        "Number of Constituencies": 5,
        "Region": "Rift Valley",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "Bomet": {
        "Population": "875,689",
        "Area": "2,631.0 km²",
        "Governor": "Hillary Barchok",
        "Literacy Level": "67%",
        "Annual Revenue": "KES 4.2 billion",
        "Annual Budget Allocation": "KES 5.5 billion",
        "Number of Constituencies": 5,
        "Region": "Rift Valley",
        "Persons with Disability": "14,000",
        "Uwezo Fund Disbursement": "KES 50 million"
    },
    "Kakamega": {
        "Population": "1,867,579",
        "Area": "3,034.4 km²",
        "Governor": "Wycliffe Oparanya",
        "Literacy Level": "67%",
        "Annual Revenue": "KES 8.4 billion",
        "Annual Budget Allocation": "KES 10.8 billion",
        "Number of Constituencies": 12,
        "Region": "Western",
        "Persons with Disability": "25,000",
        "Uwezo Fund Disbursement": "KES 100 million"
    },
    "Vihiga": {
        "Population": "612,690",
        "Area": "531.3 km²",
        "Governor": "Wilberforce Otichilo",
        "Literacy Level": "66%",
        "Annual Revenue": "KES 3.7 billion",
        "Annual Budget Allocation": "KES 4.8 billion",
        "Number of Constituencies": 5,
        "Region": "Western",
        "Persons with Disability": "11,000",
        "Uwezo Fund Disbursement": "KES 40 million"
    },
    "Bungoma": {
        "Population": "1,670,570",
        "Area": "3,032.2 km²",
        "Governor": "John Wambora",
        "Literacy Level": "65%",
        "Annual Revenue": "KES 7.8 billion",
        "Annual Budget Allocation": "KES 10.1 billion",
        "Number of Constituencies": 12,
        "Region": "Western",
        "Persons with Disability": "22,000",
        "Uwezo Fund Disbursement": "KES 85 million"
    },
    "Busia": {
        "Population": "893,681",
        "Area": "1,628.3 km²",
        "Governor": "Sospeter Ojaamong",
        "Literacy Level": "62%",
        "Annual Revenue": "KES 4.5 billion",
        "Annual Budget Allocation": "KES 5.8 billion",
        "Number of Constituencies": 7,
        "Region": "Western",
        "Persons with Disability": "15,000",
        "Uwezo Fund Disbursement": "KES 55 million"
    },
    "Siaya": {
        "Population": "1,254,817",
        "Area": "2,530.5 km²",
        "Governor": "Cornel Rasanga",
        "Literacy Level": "64%",
        "Annual Revenue": "KES 6.0 billion",
        "Annual Budget Allocation": "KES 7.7 billion",
        "Number of Constituencies": 6,
        "Region": "Nyanza",
        "Persons with Disability": "18,000",
        "Uwezo Fund Disbursement": "KES 70 million"
    },
    "Kisumu": {
        "Population": "1,155,574",
        "Area": "2,009.5 km²",
        "Governor": "Anyang' Nyong'o",
        "Literacy Level": "69%",
        "Annual Revenue": "KES 6.0 billion",
        "Annual Budget Allocation": "KES 7.8 billion",
        "Number of Constituencies": 7,
        "Region": "Nyanza",
        "Persons with Disability": "19,000",
        "Uwezo Fund Disbursement": "KES 75 million"
    },
    "Homa Bay": {
        "Population": "1,131,950",
        "Area": "3,183.3 km²",
        "Governor": "Cyprian Awiti",
        "Literacy Level": "58%",
        "Annual Revenue": "KES 5.5 billion",
        "Annual Budget Allocation": "KES 7.2 billion",
        "Number of Constituencies": 8,
        "Region": "Nyanza",
        "Persons with Disability": "17,000",
        "Uwezo Fund Disbursement": "KES 65 million"
    },
    "Migori": {
        "Population": "1,116,436",
        "Area": "2,597.9 km²",
        "Governor": "Zachary Okoth Obado",
        "Literacy Level": "63%",
        "Annual Revenue": "KES 5.0 billion",
        "Annual Budget Allocation": "KES 6.5 billion",
        "Number of Constituencies": 8,
        "Region": "Nyanza",
        "Persons with Disability": "16,000",
        "Uwezo Fund Disbursement": "KES 60 million"
    },
    "Kisii": {
        "Population": "1,266,860",
        "Area": "1,317.9 km²",
        "Governor": "James Ongwae",
        "Literacy Level": "70%",
        "Annual Revenue": "KES 6.5 billion",
        "Annual Budget Allocation": "KES 8.5 billion",
        "Number of Constituencies": 9,
        "Region": "Nyanza",
        "Persons with Disability": "20,000",
        "Uwezo Fund Disbursement": "KES 80 million"
    },
    "Nyamira": {
        "Population": "605,576",
        "Area": "912.5 km²",
        "Governor": "Amos Nyaribo",
        "Literacy Level": "68%",
        "Annual Revenue": "KES 3.5 billion",
        "Annual Budget Allocation": "KES 4.6 billion",
        "Number of Constituencies": 6,
        "Region": "Nyanza",
        "Persons with Disability": "10,000",
        "Uwezo Fund Disbursement": "KES 40 million"
    },
    "Nairobi": {
        "Population": "4,397,073",
        "Area": "696.2 km²",
        "Governor": "Johnson Sakaja",
        "Literacy Level": "79%",
        "Annual Revenue": "KES 15.6 billion",
        "Annual Budget Allocation": "KES 19.8 billion",
        "Number of Constituencies": 17,
        "Region": "Nairobi",
        "Persons with Disability": "35,000",
        "Uwezo Fund Disbursement": "KES 150 million"}
}


def search_county():
    county_name = entry.get()
    if county_name in kenya_counties:
        county_data = kenya_counties[county_name]
        result_label.config(text=f"Population: {county_data['Population']}, \n Area: {county_data['Area']}, \n Governor: {county_data['Governor']}, \n Literacy Level: {county_data['Literacy Level']}, \n Annual Revenue: {county_data['Annual Revenue']}, \n Annual Budget Allocation: {county_data['Annual Budget Allocation']}, \n Number of Constituencies: {county_data['Number of Constituencies']}, \n Persons with Disability: {county_data['Persons with Disability']}, \n Uwezo Fund Disbursement: {county_data['Uwezo Fund Disbursement']}, \n Region: {county_data['Region']}")
    else:
        result_label.config(text="Sorry, County not found! Capitalize first letter.")
        
def exit_button():
    root.destroy()


root = tk.Tk()
root.title("Kenya County Search")

custom_font = Font(family="Arial", size=12, weight="bold")

label = tk.Label(root, text="Enter County Name:", font=custom_font)
label.pack()
entry = tk.Entry(root)
entry.pack(pady=20)

search_button = tk.Button(root, text="Search", command=search_county)
search_button.pack(pady=20)


result_label = tk.Label(root, text="")
result_label.pack(pady=20)


button_exit = tk.Button(root, text="Exit", command=root.destroy)
button_exit.pack(pady=20)



root.mainloop()