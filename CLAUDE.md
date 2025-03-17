# Context of the project

this project is a platform that automates the management of car parts orders that are received through whatsapp in the spanish market. Mechanics write messages to retailers with pictures of the part, pictures of the car, of the plate, asking for different parts, then the mechanic can change its mind and amend the orders... It is clearly an issue because th retailer has to do this simultanusly for multiple mechanics, and then search in the platform is they have it, answer and process orders.

The idea of the project is to use multimodal LLM to parse the unstructured real time chat into a structured format that can be easily integrated into digital infrastructure. Then show the mechanic in real time what his whatsapp is receiving, and showing the plate, orders, and the reference number of the parts (next release tho)

# STATE of the project
the project currently, has a server and a frontend, this is the frontend evindetly. it receives the parsed status of the messages, so it simply lets the user login with its phone number and a password (login.html, then there is a page where the user can see all its cllients (clients.html) where is simply the the different whatsapp number that have written him (the mechanics), anotther screen shows the available data of the order, which consists of the car plate that the mechanic is asking about with the car brand and the car model, the parts that is asking for, and reference media pictures which can be the images of the car or the car part. Of course, lading and privacy policy page that are used for showing the project


# AIM
Its a POC so core focus is simply shipping fast, while of course avoiding shitty code although is not that big of a issue. That is why right now it does not have intricate structure because im prioritizing lightweight that is easy to extend with new things.
