from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher
import spacy
from rasa_sdk.forms import FormAction
import aiohttp
import asyncio
from templates.Web import QuickReply, Carousel
from templates.client_api import search, fetch_category_image
from templates.client_credentials import STORE_URL, STORE_NAME, PASSWORD, API_VERSION, API_KEY

nlp = spacy.load("en_core_web_md")


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = "Hi Welcome to Vanity Wagon,<br> Please tell me how can i help you."
        menu = [
            ("🔎 Explore Products", "postback", "/explore_products"),
            ("🛒 Cart", "web_url", "https://www.vanitywagon.in/cart/"),
            ("⭐ Customer reviews", "postback", "/customer_review"),
            ("🖊️ Register Complain", "postback", "/register_complain"),
            # ("💭 Quiz","postback", "/quiz"),
            ("🔎 Track Order", "postback", "/track_order"),
        ]
        qr = QuickReply.QuickReply()
        for item in menu:
            if item[1] == "postback":
                qr.add_generic_(
                    type="postback",
                    text=text,
                    title=item[0],
                    payload=item[2]
                )
            else:
                qr.add_generic_(
                    type="web_url",
                    text=text,
                    title=item[0],
                    web_url=item[2],
                    extension=False,
                )
        dispatcher.utter_message(json_message=qr.get_qr())

        return []


class ActionFallback(Action):

    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doc = nlp(tracker.latest_message["text"])

        noun = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"]]
        # No noun found in user input
        if len(noun) == 0:
            text = "I am sorry, I couldn't help you with that.<br>Try something else!"
            qr = QuickReply.QuickReply()
            qr.add_postback(text=text, title="Start Again", payload="/greet")
            message = qr.get_qr()
            dispatcher.utter_message(json_message=message)
            return []
        products = search(' '.join([str(elem) for elem in noun]))
        if not products:
            text = "I am sorry, I couldn't help you with that.<br>Try something else!"
            qr = QuickReply.QuickReply()
            qr.add_postback(text=text, title="Start Again", payload="/greet")
            message = qr.get_qr()
            dispatcher.utter_message(json_message=message)
            return []
        print(products)
        carousel = Carousel.Carousel()
        text = "Well you can have look on below products."
        dispatcher.utter_message(text=text)
        for idx in range(8):
            carousel.add_element(
                image_url=products[idx]["image"],
                title=products[idx]["title"],
                default_action_url=STORE_URL + products[idx]["url"],
                buttons=[{
                    "title": "Buy now",
                    "type": "web_url",
                    "url": STORE_URL + products[idx]['url']
                }],
                caption=f"₹{products[idx]['price']} | Type: {products[idx]['type']}"
            )
        dispatcher.utter_message(json_message=carousel.get_message())

        return []


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hi, Welcome to Vanity Wagon,<br>What would You like to do today?")

        return []


class ActionTesting(Action):

    def name(self) -> Text:
        return "action_testing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="ok")

        return []


class ActionCustomerReview(Action):

    def name(self) -> Text:
        return "action_customer_review"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = "Please have look on what our customers are sayings."
        carousel = Carousel.Carousel()
        dispatcher.utter_message(text=text)
        youtube_videos = [
            (
                "https://www.youtube.com/watch?v=kJuO2gAwH5s",
                "https://i.ytimg.com/an_webp/kJuO2gAwH5s/mqdefault_6s.webp?du=3000&sqp=CI6hn4AG&rs"
                "=AOn4CLCoWdwiPBcbXQf1GhfxgoW35l55WQ ",
                "Lipstick Swatches and Review | Disguise Cosmetics | Vanity Wagon"
            ),
            (
                "https://www.youtube.com/watch?v=eVTeQwcYNUA",
                "https://i.ytimg.com/an_webp/eVTeQwcYNUA/mqdefault_6s.webp?du=3000&sqp=CMCGn4AG&rs"
                "=AOn4CLAZkZCjRxGPa12b4uMyXgTfZJoxjg ",
                "India's Best Organic Beauty Subscription Box | Unboxing & Review | Bellebox by Vanity Wagon"
            ),
            (
                "https://www.youtube.com/watch?v=pkYU7pDIpPU",
                "https://i.ytimg.com/an_webp/pkYU7pDIpPU/mqdefault_6s.webp?du=3000&sqp=CN-Tn4AG&rs=AOn4CLCgoWf"
                "-SsD1SPhFHZGKg8VY8yPejg ",
                "Disguise Cosmetics Lip ream Swatches and Review | Vegan & Cruelty Free | Vanity Wagon",

            ),
            (
                "https://www.youtube.com/watch?v=lzgobAmFGXM",
                "https://i.ytimg.com/an_webp/8MKArQjHL50/mqdefault_6s.webp?du=3000&sqp=CN-Sn4AG&rs"
                "=AOn4CLCivmJVf6BVJHsWZ13V8oTnnXcwhQ ",
                "Glowing skin with AULI products"
            ),
            (
                "https://www.youtube.com/watch?v=8MKArQjHL50",
                "https://i.ytimg.com/an_webp/lzgobAmFGXM/mqdefault_6s.webp?du=3000&sqp=CK6Xn4AG&rs"
                "=AOn4CLAibEnH40dEJkAH203u4EfbdHASLg ",
                "Full Face Makeup Using MyGlamm | Paraben Free Makeup | Vanity Wagon",
            ),
            (
                "https://www.youtube.com/watch?v=TCG2gpAL_ug",
                "https://i.ytimg.com/an_webp/TCG2gpAL_ug/mqdefault_6s.webp?du=3000&sqp=COivn4AG&rs"
                "=AOn4CLCeGSq36F7JRhTLvcLtuc8Z5X2Knw ",
                "Story of Vanity Wagon | From the Founder"
            ),
        ]
        for idx, item in enumerate(youtube_videos):
            carousel.add_element(
                image_url=item[1],
                title=item[2],
                default_action_url=item[2],
                buttons=[{
                    "title": "🎥 Watch",
                    "type": "web_url",
                    "url": item[2]
                }],
                caption=f""
            )
        dispatcher.utter_message(json_message=carousel.get_message())

        text = "What else i can help you with? "
        menu = [
            # ("🔎 Explore Products", "postback", "/explore_products"),
            ("🛒 Cart", "web_url", "https://www.vanitywagon.in/cart/"),
            ("⭐ Customer reviews", "postback", "/customer_review"),
            ("🖊️ Register Complain", "postback", "/register_complain"),
            # ("💭 Quiz","postback", "/quiz"),
            ("🔎 Track Order", "postback", "/track_order"),
        ]
        qr = QuickReply.QuickReply(text=text)
        for item in menu:
            if item[1] == "postback":
                qr.add_generic_(
                    type="postback",
                    text=text,
                    title=item[0],
                    payload=item[2]
                )
            else:
                qr.add_generic_(
                    type="web_url",
                    text=text,
                    title=item[0],
                    web_url=item[2],
                    extension=False
                )
        dispatcher.utter_message(json_message=qr.get_qr())

        return []


class ActionExploreProducts(Action):

    def name(self) -> Text:
        return "action_explore_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = "Please have a look on the below collection, we are sure we know your choice."
        dispatcher.utter_message(text=text)
        cr = Carousel.Carousel()
        category = [
            ("BODY CARE", "https://vanitywagon.in/collections/body-care/", "183390240907"),
            ("HAIR CARE", "https://vanitywagon.in/collections/hair-care/", "183632363659"),
            ("FACE CARE", "https://vanitywagon.in/collections/face-care/", "183398367371"),
            ("MAKEUP", "https://vanitywagon.in/collections/makeup/", "183400300683"),
            ("OILS", "https://vanitywagon.in/collections/oils/", "183405805707"),
            ("MOM & BABY", "https://vanitywagon.in/collections/mom-baby/", "199181795482"),
            # ("WELLNESS", "https://vanitywagon.in/collections/wellness/", "")
        ]
        images = fetch_category_image([item[2] for item in category])
        for idx, item in enumerate(category):
            cr.add_element(
                title=item[0],
                image_url=images[idx],
                buttons=[{
                    "type": "web_url",
                    "url": item[1],
                    "title": "Show"
                }]
            )

        dispatcher.utter_message(json_message=cr.get_message())
        # Show menu after products
        text = "What else i can help you with? "
        menu = [
            # ("🔎 Explore Products", "postback", "/explore_products"),
            ("🛒 Cart", "web_url", "https://www.vanitywagon.in/cart/"),
            ("⭐ Customer reviews", "postback", "/customer_review"),
            ("🖊️ Register Complain", "postback", "/register_complain"),
            # ("💭 Quiz","postback", "/quiz"),
            ("🔎 Track Order", "postback", "/track_order"),
        ]
        qr = QuickReply.QuickReply(text=text)
        for item in menu:
            if item[1] == "postback":
                qr.add_generic_(
                    type="postback",
                    text=text,
                    title=item[0],
                    payload=item[2]
                )
            else:
                qr.add_generic_(
                    type="web_url",
                    text=text,
                    title=item[0],
                    web_url=item[2],
                    extension=False
                )
        dispatcher.utter_message(json_message=qr.get_qr())

        return []


class RegisterComplain(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "form_register_complain"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["phone_number", "email", "complain_subject", "complain_details"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "phone_number": [
                self.from_text()
            ],
            "email": [
                self.from_text()
            ],
            "complain_subject": [
                self.from_text()
            ],
            "complain_details": [
                self.from_text()
            ],
        }

    def validate_phone_number(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate phone_number"""

        text = value
        num = ""
        for car in text:
            if car.isdigit():
                print(car)
                num += car
        if len(num) <= 9:
            return {
                "phone_number": None
            }
        else:
            return {
                "phone_number": num[-10:]
            }

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """"Validate Email"""

        doc = nlp(value)
        for token in doc:
            if token.like_email:
                return {
                    "email": token.text
                }

        return {
            "email": None
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        phone_number = tracker.get_slot("phone_number")
        email = tracker.get_slot("email")
        complain_subject = tracker.get_slot("complain_subject")
        complain_details = tracker.get_slot("complain_details")

        # TODO: Call complain registration api here

        text = "Thank you for taking the time to write to us, we will get in touch with you soon."
        qr = QuickReply.QuickReply(text=text)
        menu = [
            ("🔎 Explore Products", "postback", "/explore_products"),
            ("🛒 Cart", "web_url", "https://www.vanitywagon.in/cart/"),
            ("⭐ Customer reviews", "postback", "/customer_review"),
            ("🔎 Track Order", "postback", "/track_order"),
        ]
        for item in menu:
            if item[1] == "postback":
                qr.add_generic_(
                    type="postback",
                    title=item[0],
                    payload=item[2]
                )
            else:
                qr.add_generic_(
                    type="web_url",
                    title=item[0],
                    web_url=item[2],
                    extension=False
                )
        dispatcher.utter_message(json_message=qr.get_qr())

        return []


class TrackerOrder(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "form_track_order"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["order_id"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "order_id": [
                self.from_text()
            ],
        }

    def validate_order_id(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates order_id"""

        text = value
        order_id = ""
        for char in text:
            if char.isdigit():
                order_id += char
        if order_id == "":
            return {
                "order_id": None
            }
        return {
            "order_id": order_id
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        order_id = tracker.get_slot("order_id")

        # TODO: Call shipway api here to track order

        text = f"This feature is still under development<br>Order Id:{order_id}"
        dispatcher.utter_message(text=text)
        return []


class CreateCustomer(FormAction):

    def __init__(self):
        self.counter = {
            "name": 0,  # slot_name: counter
            "phone_number": 0,
            "email": 0,
        }

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "form_create_customer"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["name", "phone_number", "email"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "name": [
                self.from_text()
            ],
            "phone_number": [
                self.from_text()
            ],
            "email": [
                self.from_text()
            ],
        }

    def validate_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates order_id"""

        text = nlp(value)
        name = list()
        for entity in text.ents:
            if entity.label_ == "PERSON":
                name.append(entity.text)

        if not name:
            return {
                "name": None
            }

        # TODO: Write code for first_name, last_name
        if len(name[0].split) >= 2:
            return {
                "name": name[0]
            }


    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        order_id = tracker.get_slot("order_id")

        # TODO: Call shipway api here to track order

        text = f"This feature is still under development<br>Order Id:{order_id}"
        dispatcher.utter_message(text=text)
        return []

