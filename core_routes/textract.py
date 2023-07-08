import boto3 
import os
from dotenv import load_dotenv
import re
import datetime
from core_routes.models import Conversions
class TextractWrapper:
    """Encapsulates Textract functions."""
    def __init__(self):
        """
        :param textract_client: A Boto3 Textract client.
        :param s3_resource: A Boto3 Amazon S3 resource.
        :param sqs_resource: A Boto3 Amazon SQS resource.
        """
        load_dotenv()
        AWS_KEY = os.getenv('AWS_KEY')
        AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
        self.INVOICE_NUMBER_ALIAS = "INVOICE_NUMBER"
        self.INVOICE_DATE_ALIAS = "INVOICE_DATE"
        self.INVOICE_TOTAL_HT_ALIAS = "INVOICE_HT_TOTAL"
        self.INVOICE_TOTAL_TTC_ALIAS = "INVOICE_TTC_TOTAL"
        self.ITEM_UNIT_SUFFIX = "UNIT"
        self.ITEM_UNIT_PRICE_SUFFIX = "UNIT_PRICE"
        self.ITEM_QUANTITY_SUFFIX = "QUANTITY"
        self.client = boto3.client('textract', region_name='eu-west-3', aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET_KEY)

    def generate_queries(self, commande):
        queries = [{
                "Text": "Quel est le numero de facture ?",
                "Alias": self.INVOICE_NUMBER_ALIAS,
                "Pages":["*"]
            },
            {
                "Text": "Quel est le total HT de la facture ?",
                "Alias": self.INVOICE_TOTAL_HT_ALIAS,
                "Pages":["*"]
            },
            {
                "Text": "Quelle est la date de la facture ?",
                "Alias": self.INVOICE_DATE_ALIAS,
                "Pages":["*"]
            },
            {
                "Text": "Quel est le total TTC de la facture ?",
                "Alias": self.INVOICE_TOTAL_TTC_ALIAS,
                "Pages":["*"]
            }
            ]
        for item in commande.items.all():
            item_name = self.remove_french(item.produit.ingredient.name)
            # item_name_for_alias = item.produit.ingredient.name.replace(" ","_")
            queries.append({
                "Text": f"Quel est le prix unitaire du {item_name} ?",
                "Alias": f"{item.id}_{self.ITEM_UNIT_PRICE_SUFFIX}",
                "Pages":["*"]
                
            })
            queries.append({
                "Text": f"Quelle est la quantite du {item_name} ?",
                "Alias": f"{item.id}_{self.ITEM_QUANTITY_SUFFIX}",
                "Pages":["*"]
            })
            queries.append({
                "Text": f"Quelle est l'unite du {item_name} ?",
                "Alias": f"{item.id}_{self.ITEM_UNIT_SUFFIX}",
                "Pages":["*"]
            })
        return {"Queries":queries}
        
    def analyze_file(
            self,commande,document_bytes=None):
        response = self.client.analyze_document(Document={'Bytes': document_bytes.file.read()},FeatureTypes = ['QUERIES'],QueriesConfig=self.generate_queries(commande))
        question_blocks = self.extract_question_blocks(response)
        answer_blocks = self.extract_answer_blocks(response)
        data = {}
        data['total_ht'] = self.get_answer_for_alias_with_number_extraction(question_blocks,answer_blocks,self.INVOICE_TOTAL_HT_ALIAS)
        data['invoice_number'] = self.get_answer_for_alias(question_blocks,answer_blocks,self.INVOICE_NUMBER_ALIAS)
        data['invoice_date'] = self.get_answer_for_alias_with_date(question_blocks,answer_blocks,self.INVOICE_DATE_ALIAS)
        data['total_ttc'] = self.get_answer_for_alias_with_number_extraction(question_blocks,answer_blocks,self.INVOICE_TOTAL_TTC_ALIAS)
        invoice_items = []
        for item in commande.items.all():
            if item:
                invoice_items.append(self.extract_item(item,question_blocks,answer_blocks))
        data['items'] = invoice_items
        return data
    

    def get_answer_id_for_alias(self, questions, alias):
        for question in questions:
            if question['Query']['Alias'] and question['Query']['Alias'] == alias:
                if 'Relationships' in question:
                    for relationship in question['Relationships']:
                        if relationship['Type'] and relationship['Type'] == 'ANSWER' and relationship['Ids'][0]:
                            return relationship['Ids'][0]
                else:
                    return None
                
    def get_answer_for_alias(self,questions,answers,alias):
        answer_id = self.get_answer_id_for_alias(questions, alias)
        for answer in answers:
            if answer['Id'] and  answer['Id'] == answer_id:
                return {'answer':answer['Text'],'confidence':answer['Confidence']}

    def get_answer_for_alias_with_number_extraction(self,questions,answers,alias):
        answer_id = self.get_answer_id_for_alias(questions, alias)
        for answer in answers:
            if answer['Id'] and  answer['Id'] == answer_id:
                try:
                    return {'answer':float("".join(re.findall("(?:^|[^\d,.])\d+(?:[,.]\d+)?(?:$|[^\d,.])",answer['Text'].replace(" ",""))).replace(",",".")),'confidence':answer['Confidence']}
                except Exception as e:
                    return {'answer':answer['Text'],'confidence':answer['Confidence']}
    
    def get_answer_for_alias_with_date(self,questions,answers,alias):
        answer_id = self.get_answer_id_for_alias(questions, alias)
        for answer in answers:
            if answer['Id'] and  answer['Id'] == answer_id:
                try: 
                    return {'answer':datetime.datetime.strptime(answer['Text'], "%d/%m/%Y").date(),'confidence':answer['Confidence']}
                    
                except:
                    return {'answer':answer['Text'],'confidence':answer['Confidence']}

    def extract_item(self, item, questions, answers):
        item_data = {'id':item.id,'name':item.produit.ingredient.name,'unit':item.unit}
        unit = self.get_answer_for_alias(questions,answers,f"{item.id}_{self.ITEM_UNIT_SUFFIX}")
        unit_price = self.get_answer_for_alias_with_number_extraction(questions,answers,f"{item.id}_{self.ITEM_UNIT_PRICE_SUFFIX}")
        quantity = self.get_answer_for_alias_with_number_extraction(questions,answers,f"{item.id}_{self.ITEM_QUANTITY_SUFFIX}")
        same_unit = True
        if unit:
            if self.units_are_same(unit['answer'],item.unit) or unit['confidence']<45:
                item_data['unit_is_same']=True
                if unit_price:
                    item_data['unit_price']=unit_price
                else: 
                    item_data['unit_price'] = {}
                if quantity:
                    item_data['quantity']=quantity
                else: 
                    item_data['quantity'] = {}
            else:
                same_unit = False
        else:
            same_unit = False    
        if not same_unit:
            item_data['unit_is_same']=False
            if unit_price:
                item_data['unit_price']=unit_price
            else: 
                item_data['unit_price'] = {}
            if quantity:
                item_data['quantity']=quantity
                item_data['quantity']['answer']/= float(item.unit_quantity)
            else: 
                item_data['quantity'] = {}
            item_data['unit_quantity']=item.unit_quantity
            ingredient = item.produit.ingredient
            possible_units = ["kilogramme"]
            if ingredient.unit != "kilogramme":
                possible_units.append(ingredient.unit)
            try:
                recorded_conversions = Conversions.objects.filter(ingredient=ingredient)
                for conversion in recorded_conversions:
                    possible_units.append(conversion.unit)
            except Exception as e:
                print(f"Error generating units list: {e}")
            item_data['possible_units']=possible_units
        return item_data
    
    def units_are_same(self, unit_1, unit_2):
        unit_1 = unit_1.lower()
        unit_2 = unit_2.lower()
        return self.remove_french(unit_1) == self.remove_french(unit_2) or unit_1 == "kilogramme" and unit_2 == "kg" or unit_1=="kg" and unit_2 == "kilogramme" or  unit_1=="l" and unit_2 == "littre" or  unit_1=="littre" and unit_2 == "l" or  unit_1=="gramme" and unit_2 == "g" or  unit_1=="g" and unit_2 == "gramme" or  unit_1=="pce" and unit_2 == "pièce" or  unit_1=="pièce" and unit_2 == "pce" or  unit_1=="pce" and unit_2 == "unité" or  unit_1=="unité" and unit_2 == "pce" or  unit_1=="pièce" and unit_2 == "unité"or  unit_1=="unité" and unit_2 == "pièce"
    def extract_question_blocks(self,output):
        return self.extract_block_type(output,"QUERY")
    
    def extract_answer_blocks(self,output):
        return self.extract_block_type(output,"QUERY_RESULT")
    
    def extract_block_type(self,output,type):
        blocks_of_type = []
        for block in output["Blocks"]:
            if block["BlockType"] == type:
                blocks_of_type.append(block)
        return blocks_of_type

    def remove_french(self,string):
        return string.replace("é", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace("î", "i").replace("ê", "e")