# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import SlotSet, EventType

sanf_ask_trait = False
sanf_ask_subject = False
soft_eng_asked = False

stnf_ask_trait = False
stnf_ask_subject = False

unk1_ask_subject = False
unk1_ask_trait = False
unk1_excluded_subject = set()
unk1_excluded_trait = set()

unk2_ask_subject = False
unk2_ask_trait = False
unk2_excluded_subject = set()
unk2_excluded_trait = set()

unk3_ask_subject = False
unk3_ask_trait = False
unk3_excluded_subject = set()
unk3_excluded_trait = set()

unk4_ask_subject = False
unk4_ask_trait = False
unk4_excluded_subject = set()
unk4_excluded_trait = set()

unk_ask_subject = False
unk_ask_trait = False
unk_excluded_subject = set()
unk_excluded_trait = set()

class ActionSetProf(Action):

     def name(self) -> Text: 
         return "action_set_prof"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[EventType]:
         
         # INITIAL FORM
         if tracker.get_slot('prof_name') is None:
            #for all professors who fit the criteria:
            #hair: short, height: ave, glasses: no, position: faculty (SANF)
            if (tracker.get_slot('hair') == "short" 
                and tracker.get_slot('height') == "ave"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "faculty"
                ):
                
                global sanf_ask_subject
                global sanf_ask_trait
                global soft_eng_asked

                global stnf_ask_subject
                global stnf_ask_trait

                # sanf teaches yr 1
                if (tracker.get_slot('year1')) and (sanf_ask_trait == False):
                    # sanf manages comlab
                    sanf_ask_trait = True
                    dispatcher.utter_message(response="utter_ask_trait_comlab")
                    return []
                
                elif (tracker.get_slot('year1')) and (sanf_ask_trait == True): 
                    sanf_ask_trait = False
                    return[SlotSet("prof_name","lagunzad")]

                # sanf teaches yr 2   
                elif (tracker.get_slot('year2')) and (sanf_ask_subject == False):
                    sanf_ask_subject == True
                    dispatcher.utter_message(response="utter_ask_subject_opres")
                    return []

                elif (tracker.get_slot('year2')) and (sanf_ask_subject == True):
                    # sanf teaches opres
                    if tracker.get_slot('subject') == "opres":
                        sanf_ask_subject = False
                        return[SlotSet("prof_name","maborang")]
                    # sanf teaches else (ias)
                    else:
                        sanf_ask_subject = False
                        return[SlotSet("prof_name","canlas")]

                #sanf teaches yr 3
                elif (tracker.get_slot('year3')) and (sanf_ask_subject == False):
                    #sanf teaches automata
                    sanf_ask_subject = True
                    dispatcher.utter_message(response="utter_ask_subject_automata")
                    return []
                
                elif (tracker.get_slot('year3')) and (sanf_ask_subject == True):
                    
                    if tracker.get_slot('subject') == "automata": 
                        sanf_ask_subject = False
                        return[SlotSet("prof_name","mahusay")]
                    
                    elif soft_eng_asked == True:
                        #sanf teaches soft_eng
                        if tracker.get_slot('subject') == "soft_eng":
                            sanf_ask_subject = False
                            soft_eng_asked = False
                            return[SlotSet("prof_name","morano")]
                        #sanf doesn't teach soft_eng
                        else:
                            sanf_ask_subject = False
                            soft_eng_asked = False
                            return[SlotSet("prof_name","contreras")]
                    else:
                        #ask if sanf teaches soft_eng
                        sanf_ask_subject = True
                        soft_eng_asked = True
                        dispatcher.utter_message(response="utter_ask_subject_softeng")
                        return []
                            
                #sanf teaches yr 4            
                elif tracker.get_slot('year4'): return[SlotSet("prof_name","canlas")]
                    
                
            #for all professors who fit the criteria:
            #hair: short, height: tall, glasses: no, position: faculty (STNF)    
            elif (tracker.get_slot('hair') == "short" 
                and tracker.get_slot('height') == "tall"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "faculty"
                ):
                
                #stnf teaches yr 1
                if tracker.get_slot('year1'): return[SlotSet("prof_name","tenio")]

                #stnf teaches yr 2
                elif (tracker.get_slot('year2')) and (stnf_ask_subject == False):
                    stnf_ask_subject = True
                    dispatcher.utter_message(response="utter_ask_subject_infoman")
                    return []
                
                elif (tracker.get_slot('year2')) and (stnf_ask_subject == True):
                    #stnf teaches infoman
                    if tracker.get_slot('subject') == "info_man":
                        stnf_ask_subject == False
                        return[SlotSet("prof_name","genota")]
                    else: 
                        stnf_ask_subject == False
                        return[SlotSet("prof_name","kawabata")]
                    
                #stnf teaches yr 3    
                elif tracker.get_slot('year3'): return[SlotSet("prof_name","cruz")]
                
                #stnf teaches yr 4
                elif (tracker.get_slot('year4')) and (stnf_ask_subject == False):
                    #ask stnf teaches thesis
                    stnf_ask_subject == True
                    dispatcher.utter_message(response="utter_ask_subject_thesis")
                    return []
                    #stnf teaches thesis
                    
                elif (tracker.get_slot('year4')) and (stnf_ask_subject == True):
                    if tracker.get_slot('subject') == "thesis":
                        stnf_ask_subject == False
                        return[SlotSet("prof_name","cruz")]
                    
                    elif stnf_ask_trait == True: 
                        #stnf owns unique trait cybersec_cert
                        if tracker.get_slot('trait') == "cybersec_cert":
                            stnf_ask_subject == False
                            return[SlotSet("prof_name","kawabata")]
                        else: 
                            stnf_ask_subject == False
                            return[SlotSet("prof_name","tenio")]
                    else:
                        stnf_ask_trait = True
                        dispatcher.utter_message(response="utter_ask_trait_cybersec_cert")
                        return[]
                        
            #Past this are a combination of traits that are unique to one prof -------------------------
            
            #prof agustin
            elif (tracker.get_slot('hair') == "long" 
                and tracker.get_slot('height') == "ave"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "chairperson"
                ): return[SlotSet("prof_name","agustin")]

            #prof guialil
            elif (tracker.get_slot('hair') == "long" 
                and tracker.get_slot('height') == "ave"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "faculty"
                ):
                if ((tracker.get_slot('trait') is None)
                    or (tracker.get_slot('trait') == "unknown")):
                    return[SlotSet("prof_name","guialil")]
                
            #prof dioses
            elif (tracker.get_slot('hair') == "short" 
                and tracker.get_slot('height') == "ave"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "chairperson"
                ): return[SlotSet("prof_name","dioses")]
            
            #prof pineda
            elif (tracker.get_slot('hair') == "long" 
                and tracker.get_slot('height') == "tall"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "faculty"
                ): return[SlotSet("prof_name","pineda")]
            
            #prof cortez
            elif (tracker.get_slot('hair') == "short" 
                and tracker.get_slot('height') == "tall"
                and tracker.get_slot('glasses') == "no"
                and tracker.get_slot('position') == "chairperson"
                ): return[SlotSet("prof_name","cortez")]
            
            #prof pascual
            elif (tracker.get_slot('hair') == "long" 
                and tracker.get_slot('height') == "ave"
                and tracker.get_slot('glasses') == "yes"
                and tracker.get_slot('position') == "faculty"
                ): return[SlotSet("prof_name","pascual")]
            
            #prof atienza
            elif (tracker.get_slot('hair') == "short" 
                and tracker.get_slot('height') == "tall"
                and tracker.get_slot('glasses') == "yes"
                and tracker.get_slot('position') == "faculty"
                ):
                return[SlotSet("prof_name","atienza")]
            
            #if user doesn't know phys appearance -------------------------------------------------------
            elif (tracker.get_slot('hair') == "unknown" 
                or tracker.get_slot('height') == "unknown" 
                or tracker.get_slot('glasses') == "unknown"
                or tracker.get_slot('position') == "unknown"
                ):

                if tracker.get_slot('year1'):
                    if unk1_ask_subject == False and unk1_ask_trait == False:
                            if "ds" not in unk1_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_ds")
                                unk1_excluded_subject.add("ds")
                                unk1_ask_subject = True
                                return []
                            elif "hci" not in unk1_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_hci")
                                unk1_excluded_subject.add("hci")
                                unk1_ask_subject = True
                                return[]
                            else:
                                unk1_ask_trait = True
                                return[]
                            
                    elif unk1_ask_subject == True and unk1_ask_trait == False:
                        match tracker.get_slot('subject'):
                            case "ds":
                                unk1_ask_subject = False
                                return[SlotSet("prof_name","lagunzad")]
                            case _:
                                unk1_ask_subject = False
                                unk1_ask_trait = True
                                return[]
                    
                    elif unk1_ask_subject == False and unk1_ask_trait == True:
                        if "cschair" not in unk1_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_cschair")
                            unk1_excluded_trait.add("cschair")
                            unk1_ask_trait = True
                            return[]
                        elif "masters" not in unk1_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_masters")
                            unk1_excluded_trait.add("masters")
                            unk1_ask_trait = True
                            return[]
                        elif "gdsc" not in unk1_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_gdsc")
                            unk1_excluded_trait.add("gdsc")
                            unk1_ask_trait = True
                            return[]
                        elif "comlab" not in unk1_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_comlab")
                            unk1_excluded_trait.add("comlab")
                            unk1_ask_trait = True
                            return[]
                        else:
                            unk1_ask_subject = False
                            unk1_ask_trait = False
                            return[SlotSet("prof_name","tenio")]
                
                elif tracker.get_slot('year2'):
                    if unk2_ask_subject == False and unk2_ask_trait == False:
                            dispatcher.utter_message(response="utter_ask_subject_opres")
                            unk2_ask_subject = True
                            return[]
                        
                    elif unk2_ask_subject == True:
                        if tracker.get_slot('subject') == "opres": 
                            unk2_ask_subject = False
                            unk2_ask_trait = True
                            return[SlotSet("prof_name","maborang")]
                        
                    elif unk2_ask_subject == False and unk2_ask_trait == True:

                        if "cs_chair" not in unk2_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_cschair")
                            unk2_excluded_trait.add("cs_chair")
                            return[]
                        
                        elif "cybersec_gov" not in unk2_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_cybersec_gov")
                            unk2_excluded_trait.add("cybersec_gov")
                            return[]
                        
                        elif "cybersec_enthu" not in unk2_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_cybersec_enthu")
                            unk2_excluded_trait.add("cybersec_enthu")
                            return[]
                        
                        elif "pastor" not in unk2_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_pastor")
                            unk2_excluded_trait.add("pastor")
                            return[]

                        elif "ibm" not in unk2_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_ibm")
                            unk2_excluded_trait.add("ibm")
                            return[]

                        else: 
                            unk2_ask_subject = False
                            unk2_ask_trait = False
                            return[SlotSet("prof_name","unknown")]

                elif tracker.get_slot('year3'):
                    if unk3_ask_subject == False and unk3_ask_trait == False:
                            if "automata" not in unk3_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_automata")
                                unk3_excluded_subject.add("automata")
                                unk3_ask_subject = True
                                return[]
                            
                            elif "proglang" not in unk3_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_proglang")
                                unk3_excluded_subject.add("proglang")
                                unk3_ask_subject = True
                                return[]
                            
                            elif "softeng" not in unk3_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_softeng")
                                unk3_excluded_subject.add("softeng")
                                unk3_ask_subject = True
                                return[]
                            
                            elif "compiler" not in unk3_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_compiler")
                                unk3_excluded_subject.add("compiler")
                                unk3_ask_subject = True
                                return[]
                            
                            elif "intsys" not in unk3_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_intsys")
                                unk3_excluded_subject.add("intsys")
                                unk3_ask_subject = True
                                return[]
                            
                            else:
                                unk3_ask_trait = True
                                return[]

                    elif unk3_ask_subject == True and unk3_ask_trait == False:
                        match tracker.get_slot('subject'):
                            case "automata": 
                                unk3_ask_subject = False
                                return[SlotSet("prof_name","mahusay")]
                            case "prog_lang":
                                unk3_ask_subject = False
                                return[SlotSet("prof_name","contreras")]
                            case "soft_eng":
                                unk3_ask_subject = False
                                return[SlotSet("prof_name","morano")]
                            case "compiler":
                                unk3_ask_subject = False
                                return[SlotSet("prof_name","pineda")]
                            case "int_sys":
                                unk3_ask_subject = False
                                return[SlotSet("prof_name","cruz")]
                            case _:
                                unk3_ask_subject = False
                                return[]
                    
                    elif unk3_ask_subject == False and unk3_ask_trait == True:

                        if "eng" not in unk3_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_eng")
                            unk3_excluded_trait.add("eng")
                            unk3_ask_trait = True
                            return[]
                        
                        elif "pastor" not in unk3_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_pastor")
                            unk3_excluded_trait.add("pastor")
                            unk3_ask_trait = True
                            return[]
                        
                        elif "ibm" not in unk3_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_ibm")
                            unk3_excluded_trait.add("ibm")
                            unk3_ask_trait = True
                            return[]
                        
                        else: 
                            unk3_ask_trait = False
                            return[SlotSet("prof_name","unknown")]
                
                elif tracker.get_slot('year4'):
                    if unk4_ask_subject == False and unk4_ask_trait == False:
                            if "thesis" not in unk4_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_thesis")
                                unk4_excluded_subject.add("thesis")
                                unk4_ask_subject = True
                                return[] 
                            elif "elec_2" not in unk4_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_elec_2")
                                unk4_excluded_subject.add("elec_2")
                                unk4_ask_subject = True
                                return []
                            elif "netcom" not in unk4_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_netcom")
                                unk4_excluded_subject.add("netcom")
                                unk1_ask_subject = True
                                return[]
                            elif "elec_3" not in unk4_excluded_subject:
                                dispatcher.utter_message(response="utter_ask_subject_elec_3")
                                unk4_excluded_subject.add("elec_3")
                                unk4_ask_subject = True
                                return[]
                            else:
                                unk4_ask_trait = True
                                return[]
                            
                    elif unk4_ask_subject == True and unk4_ask_trait == False:
                        match tracker.get_slot('subject'):
                            case "thesis":
                                unk4_ask_subject = False
                                return[SlotSet("prof_name","cruz")]
                            case "elec_2":
                                unk4_ask_subject = False
                                return[SlotSet("prof_name","guialil")]
                            case "net_com":
                                unk4_ask_subject = False
                                return[SlotSet("prof_name","canlas")]
                            case "elec_3":
                                unk4_ask_subject = False
                                unk4_ask_trait = True
                                return[]
                            case _:
                                unk4_ask_subject = False
                                return[]
                    
                    elif unk4_ask_subject == False and unk4_ask_trait == True:
                        if "cybersec_cert" not in unk4_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_cybersec_cert")
                            unk4_excluded_trait.add("cybersec_cert")
                            unk4_ask_trait = True
                            return []
                        else:
                            unk4_ask_trait = False
                            return[SlotSet("prof_name","tenio")]
                
                else:
                    if "gdsc" not in unk_excluded_trait:
                            dispatcher.utter_message(response="utter_ask_trait_gdsc")
                            unk_excluded_trait.add("gdsc")
                            return[]
                    elif "comlab" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_comlab")
                        unk_excluded_trait.add("comlab")
                        return[]
                    elif "cschair" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_cschair")
                        unk_excluded_trait.add("cschair")
                        return[]
                    elif "cybersec_gov" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_cybersec_gov")
                        unk_excluded_trait.add("cybersec_gov")
                        return[]
                    elif "masters" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_masters")
                        unk_excluded_trait.add("masters")
                        return[]
                    elif "eng" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_eng")
                        unk_excluded_trait.add("eng")
                        return[]
                    elif "cybersec_cert" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_cybersec_cert")
                        unk_excluded_trait.add("cybersec_cert")
                        return[]
                    elif "pastor" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_pastor")
                        unk_excluded_trait.add("pastor")
                        return[]
                    elif "ibm" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_ibm")
                        unk_excluded_trait.add("ibm")
                        return[]
                    elif "95" not in unk_excluded_trait:
                        dispatcher.utter_message(response="utter_ask_trait_95")
                        unk_excluded_trait.add("95")
                        return[]
                    else:
                        return[SlotSet("prof_name","unknown")]              

         else: return []      

# class ActionUtterTraitGDSC(Action):

#      def name(self) -> Text: 
#          return "action_utter_ask_trait_gdsc"

#      def run(self, dispatcher: CollectingDispatcher,
#              tracker: Tracker,
#              domain: Dict[Text, Any]) -> List[EventType]:
         
#          dispatcher.utter_message(response="utter_ask_trait_gdsc")
#          return[]

class ActionUtterProf(Action):

     def name(self) -> Text: 
         return "action_utter_prof"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[EventType]:
         
         slotProf = ""
         strProf = ""

         #dispatcher.utter_message(text="Guessing...")
         if tracker.get_slot('prof_name') is not None:
            slotProf = tracker.get_slot('prof_name')
            match slotProf:
                    case "lagunzad":
                        strProf = "Prof. Herminino Lagunzad"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "agustin":
                        strProf = "Prof. Vivien A. Agustin"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "regala":
                        strProf = "Prof. Richard C. Regala"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "dioses":
                        strProf = "Prof. Raymund Dioses"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "maborang":
                        strProf = "Prof. Romie C. Maborang"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "genota":
                        strProf = "Prof. Alvin V. Genota"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "guialil":
                        strProf = "Prof. Jamillah S. Guialil"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "kawabata":
                        strProf = "Prof. Jeffrey S. Kawabata"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "mahusay":
                        strProf = "Prof. Leisyl Mahusay"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "contreras":
                        strProf = "Prof. Jerico Contreras"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "morano":
                        strProf = "Prof. Jonathan Morano"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "cruz":
                        strProf = "Prof. Joel Cruz"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "pineda":
                        strProf = "Prof. Pineda"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "cortez":
                        strProf = "Doc. Dan Michael Cortez" #
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "tenio":
                        strProf = "Prof. John Ray Tenio"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "pascual":
                        strProf = "Prof. Elsa S. Pascual"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "atienza":
                        strProf = "Prof. Francis Atienza"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "canlas":
                        strProf = "Prof. Renz Canlas"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case "unknown":
                        strProf = "a cs professor that doesn't exist"
                        # return[dispatcher.utter_message(text="You are thinking of: "+str(strProf))]
                    case _:
                        strProf = None
                        
            sanf_ask_trait = False
            sanf_ask_subject = False
            soft_eng_asked = False

            stnf_ask_trait = False
            stnf_ask_subject = False

            unk1_ask_subject = False
            unk1_ask_trait = False
            unk1_excluded_subject = set()
            unk1_excluded_trait = set()

            unk2_ask_subject = False
            unk2_ask_trait = False
            unk2_excluded_subject = set()
            unk2_excluded_trait = set()

            unk3_ask_subject = False
            unk3_ask_trait = False
            unk3_excluded_subject = set()
            unk3_excluded_trait = set()

            unk4_ask_subject = False
            unk4_ask_trait = False
            unk4_excluded_subject = set()
            unk4_excluded_trait = set()

            unk_ask_subject = False
            unk_ask_trait = False
            unk_excluded_subject = set()
            unk_excluded_trait = set()

            dispatcher.utter_message(text="You are thinking of: "+str(strProf))
            return[]
         

# class ActionResetForm(Action):

#      def name(self) -> Text:
#          return "action_reset_form"

#      def run(self, dispatcher: CollectingDispatcher,
#              tracker: Tracker,
#              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#          dispatcher.utter_message(text="Alright, let's start over.")
#          return[SlotSet("hair",None)
#             ,SlotSet("height",None)
#             ,SlotSet("glasses",None)
#             ,SlotSet("position",None)
#             ,SlotSet("year",None)
#             ,SlotSet("subject",None)
#             ,SlotSet("trait",None)
#             ,SlotSet("excluded_traits",None)
#             ,SlotSet("excluded_years",None)
#             ,SlotSet("prof_name",None)]

# class ActionAppendExcludedTrait(Action):
#     def name(self) -> Text:
#         return "action_append_excluded_trait"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[EventType]:
        
#         # Initialize the list slot if it's not already a list
#         ex_traits = tracker.get_slot("excluded_trait")
        
#         if ex_traits is None:
#             ex_traits = []

#         # Get the trait entity from the latest message
#         ex_trait = next(tracker.get_latest_entity_values("excluded_trait"), None)

#         if ex_trait:
#             ex_traits.append(ex_trait)
        
#         return[SlotSet("excluded_traits", ex_traits)]
    
# class ActionAppendExcludedYear(Action):
#     def name(self) -> Text:
#         return "action_append_excluded_year"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[EventType]:
        
#         # Initialize the list slot if it's not already a list
#         ex_years = tracker.get_slot("excluded_year")
        
#         if ex_years is None:
#             ex_years = []

#         # Get the trait entity from the latest message
#         ex_year = next(tracker.get_latest_entity_values("excluded_year"), None)

#         if ex_year:
#             ex_years.append(ex_year)

#         return[SlotSet("excluded_years", ex_years)]




         
