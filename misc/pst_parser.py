#!/usr/bin/env python

import sys
import os
import pypff
import re

from argparse import ArgumentParser

OUTLOOK_DATA_FILE = 1
DELETED = 0
INBOX = 1

class PSTRecordEntry:
    
    # mappings for the entry type to friendly name
    entry_types = {
            0x001a: "MESSAGE_CLASS",
            0x0026: "MESSAGE_PRIORITY",
            0x0036: "MESSAGE_SENSITIVITY",
            0x0037: "MESSAGE_SUBJECT",
            0x0039: "MESSAGE_CLIENT_SUBMIT_TIME",
            0x003b: "MESSAGE_SENT_REPRESENTING_SEARCH_KEY",
            0x003f: "MESSAGE_RECEIVED_BY_ENTRY_IDENTIFIER",
            0x0040: "MESSAGE_RECEIVED_BY_NAME",
            0x0041: "MESSAGE_SENT_REPRESENTING_ENTRY_IDENTIFIER",
            0x0042: "MESSAGE_SENT_REPRESENTING_NAME",
            0x0043: "MESSAGE_RECEIVED_REPRESENTING_ENTRY_IDENTIFIER",
            0x0044: "MESSAGE_RECEIVED_REPRESENTING_NAME",
            0x004f: "MESSAGE_REPLY_RECIPIENT_ENTRIES",
            0x0050: "MESSAGE_REPLY_RECIPIENT_NAMES",
            0x0051: "MESSAGE_RECEIVED_BY_SEARCH_KEY",
            0x0052: "MESSAGE_RECEIVED_REPRESENTING_SEARCH_KEY",
            0x0064: "MESSAGE_SENT_REPRESENTING_ADDRESS_TYPE",
            0x0065: "MESSAGE_SENT_REPRESENTING_EMAIL_ADDRESS",
            0x0070: "MESSAGE_CONVERSATION_TOPIC",
            0x0071: "MESSAGE_CONVERSATION_INDEX",
            0x0075: "MESSAGE_RECEIVED_BY_ADDRESS_TYPE",
            0x0076: "MESSAGE_RECEIVED_BY_EMAIL_ADDRESS",
            0x0077: "MESSAGE_RECEIVED_REPRESENTING_ADDRESS_TYPE",
            0x0078: "MESSAGE_RECEIVED_REPRESENTING_EMAIL_ADDRESS",
            0x007d: "MESSAGE_TRANSPORT_HEADERS",
            0x0c15: "RECIPIENT_TYPE",
            0x0c19: "MESSAGE_SENDER_ENTRY_IDENTIFIER",
            0x0c1a: "MESSAGE_SENDER_NAME",
            0x0c1d: "MESSAGE_SENDER_SEARCH_KEY",
            0x0c1e: "MESSAGE_SENDER_ADDRESS_TYPE",
            0x0c1f: "MESSAGE_SENDER_EMAIL_ADDRESS",
            0x0e04: "MESSAGE_DISPLAY_TO",
            0x0e06: "MESSAGE_DELIVERY_TIME",
            0x0e07: "MESSAGE_FLAGS",
            0x0e08: "MESSAGE_SIZE",
            0x0e17: "MESSAGE_STATUS",
            0x0e20: "ATTACHMENT_SIZE",
            0x0e23: "MESSAGE_INTERNET_ARTICLE_NUMBER",
            0x0e27: "MESSAGE_PERMISSION",
            0x0e62: "MESSAGE_URL_COMPUTER_NAME_SET",
            0x0e79: "MESSAGE_TRUST_SENDER",
            0x1000: "MESSAGE_BODY_PLAIN_TEXT",
            0x1009: "MESSAGE_BODY_COMPRESSED_RTF",
            0x1013: "MESSAGE_BODY_HTML",
            0x10f3: "EMAIL_EML_FILENAME",
            0x3001: "DISPLAY_NAME",
            0x3002: "ADDRESS_TYPE",
            0x3003: "EMAIL_ADDRESS",
            0x3007: "MESSAGE_CREATION_TIME",
            0x3008: "MESSAGE_MODIFICATION_TIME",
            0x35df: "MESSAGE_STORE_VALID_FOLDER_MASK",
            0x3601: "FOLDER_TYPE",
            0x3602: "NUMBER_OF_CONTENT_ITEMS",
            0x3603: "NUMBER_OF_UNREAD_CONTENT_ITEMS",
            0x360a: "HAS_SUB_FOLDERS",
            0x3613: "CONTAINER_CLASS",
            0x3617: "NUMBER_OF_ASSOCIATED_CONTENT",
            0x3701: "ATTACHMENT_DATA_OBJECT",
            0x3704: "ATTACHMENT_FILENAME_SHORT",
            0x3705: "ATTACHMENT_METHOD",
            0x3707: "ATTACHMENT_FILENAME_LONG",
            0x370b: "ATTACHMENT_RENDERING_POSITION",
            0x3a02: "CONTACT_CALLBACK_PHONE_NUMBER",
            0x3a05: "CONTACT_GENERATIONAL_ABBREVIATION",
            0x3a06: "CONTACT_GIVEN_NAME",
            0x3a08: "CONTACT_BUSINESS_PHONE_NUMBER_1",
            0x3a09: "CONTACT_HOME_PHONE_NUMBER",
            0x3a0a: "CONTACT_INITIALS",
            0x3a11: "CONTACT_SURNAME",
            0x3a15: "CONTACT_POSTAL_ADDRESS",
            0x3a16: "CONTACT_COMPANY_NAME",
            0x3a17: "CONTACT_JOB_TITLE",
            0x3a18: "CONTACT_DEPARTMENT_NAME",
            0x3a19: "CONTACT_OFFICE_LOCATION",
            0x3a1a: "CONTACT_PRIMARY_PHONE_NUMBER",
            0x3a1b: "CONTACT_BUSINESS_PHONE_NUMBER_2",
            0x3a1c: "CONTACT_MOBILE_PHONE_NUMBER",
            0x3a24: "CONTACT_BUSINESS_FAX_NUMBER",
            0x3a26: "CONTACT_COUNTRY",
            0x3a27: "CONTACT_LOCALITY",
            0x3a45: "CONTACT_TITLE",
            0x3fde: "MESSAGE_BODY_CODEPAGE",
            0x3ffd: "MESSAGE_CODEPAGE",
            0x5ff6: "RECIPIENT_DISPLAY_NAME",
            0x6638: "FOLDER_CHILD_COUNT",
            0x67f2: "SUB_ITEM_IDENTIFIER",
            0x67ff: "MESSAGE_STORE_PASSWORD_CHECKSUM",
            0x8005: "ADDRESS_FILE_UNDER",
            0x8053: "DISTRIBUTION_LIST_NAME",
            0x8054: "DISTRIBUTION_LIST_MEMBER_ONE_OFF_ENTRY_IDENTIFIERS",
            0x8055: "DISTRIBUTION_LIST_MEMBER_ENTRY_IDENTIFIERS",
            0x8083: "CONTACT_EMAIL_ADDRESS_1",
            0x8093: "CONTACT_EMAIL_ADDRESS_2",
            0x80a3: "CONTACT_EMAIL_ADDRESS_3",
            0x8101: "TASK_STATUS",
            0x8102: "TASK_PERCENTAGE_COMPLETE",
            0x8104: "TASK_START_DATE",
            0x8105: "TASK_DUE_DATE",
            0x8110: "TASK_ACTUAL_EFFORT",
            0x8111: "TASK_TOTAL_EFFORT",
            0x8112: "TASK_VERSION",
            0x811c: "TASK_IS_COMPLETE",
            0x8126: "TASK_IS_RECURRING",
            0x8205: "APPOINTMENT_BUSY_STATUS",
            0x8208: "APPOINTMENT_LOCATION",
            0x820d: "APPOINTMENT_START_TIME",
            0x820e: "APPOINTMENT_END_TIME",
            0x8213: "APPOINTMENT_DURATION",
            0x8223: "APPOINTMENT_IS_RECURRING",
            0x8232: "APPOINTMENT_RECURRENCE_PATTERN",
            0x8234: "APPOINTMENT_TIMEZONE_DESCRIPTION",
            0x8235: "APPOINTMENT_FIRST_EFFECTIVE_TIME",
            0x8236: "APPOINTMENT_LAST_EFFECTIVE_TIME",
            0x8502: "MESSAGE_REMINDER_TIME",
            0x8503: "MESSAGE_IS_REMINDER",
            0x8506: "MESSAGE_IS_PRIVATE",
            0x8550: "MESSAGE_REMINDER_SIGNAL_TIME",        
    }
    
    # mappings to functions to retrieve the value of the entry
    value_type_funcs = {
        0x0000: lambda _: None, #LIBPFF_VALUE_TYPE_UNSPECIFIED
        0x0001: lambda _: None, #LIBPFF_VALUE_TYPE_NULL
        0x0002: pypff.record_entry.get_data_as_integer, #LIBPFF_VALUE_TYPE_INTEGER_16BIT_SIGNED
        0x0003: pypff.record_entry.get_data_as_integer, #LIBPFF_VALUE_TYPE_INTEGER_32BIT_SIGNED
        0x0004: pypff.record_entry.get_data_as_floating_point, #LIBPFF_VALUE_TYPE_FLOAT_32BIT						
        0x0005: pypff.record_entry.get_data_as_floating_point, #LIBPFF_VALUE_TYPE_DOUBLE_64BIT						
        0x0006: pypff.record_entry.get_data_as_floating_point, #LIBPFF_VALUE_TYPE_CURRENCY
        0x0007: pypff.record_entry.get_data_as_floating_point, #LIBPFF_VALUE_TYPE_FLOATINGTIME
        0x000a: pypff.record_entry.get_data, #LIBPFF_VALUE_TYPE_ERROR
        0x000b: pypff.record_entry.get_data_as_boolean, #LIBPFF_VALUE_TYPE_BOOLEAN
        0x000d: pypff.record_entry.get_data, #LIBPFF_VALUE_TYPE_OBJECT
        0x0014: pypff.record_entry.get_data_as_integer, #LIBPFF_VALUE_TYPE_INTEGER_64BIT_SIGNED
        0x001e: pypff.record_entry.get_data_as_string, #LIBPFF_VALUE_TYPE_STRING_ASCII
        0x001f: lambda x:unicode(pypff.record_entry.get_data_as_string(x)), #LIBPFF_VALUE_TYPE_STRING_UNICODE
        0x0040: pypff.record_entry.get_data_as_integer, #LIBPFF_VALUE_TYPE_FILETIME 
        0x0048: pypff.record_entry.get_data_as_string, #LIBPFF_VALUE_TYPE_GUID
        0x00fb: pypff.record_entry.get_data_as_string, #LIBPFF_VALUE_TYPE_SERVER_IDENTIFIER
        #0x00fd: pypff.record_entry.get_data, #LIBPFF_VALUE_TYPE_RESTRICTION
        #0x00fe: pypff.record_entry.get_data, #LIBPFF_VALUE_TYPE_RULE_ACTION
        #0x0102: pypff.record_entry.get_data #LIBPFF_VALUE_TYPE_BINARY_DATA 
        
        # not sure how to deal with these types yet!						
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_INTEGER_16BIT_SIGNED			: 0x1002,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_INTEGER_32BIT_SIGNED			: 0x1003,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_FLOAT_32BIT				: 0x1004,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_DOUBLE_64BIT				: 0x1005,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_CURRENCY					: 0x1006,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_FLOATINGTIME				: 0x1007,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_INTEGER_64BIT_SIGNED			: 0x1014,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_STRING_ASCII				: 0x101e,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_STRING_UNICODE				: 0x101f,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_FILETIME					: 0x1040,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_GUID					: 0x1048,
        #LIBPFF_VALUE_TYPE_MULTI_VALUE_BINARY_DATA				: 0x1102                
    }
    
    
    def __init__(self, record_entry):
        self.record_entry = record_entry

    
    def get_type(self):
        entry_type = self.record_entry.get_entry_type()
        if entry_type is None:
            return None
        
        
        if PSTRecordEntry.entry_types.has_key(entry_type):
            return PSTRecordEntry.entry_types[entry_type]
        
        return hex(entry_type)
    
    
    def get_value(self):
        val_type = self.record_entry.get_value_type()
        if val_type is None:
            return None
        
        if PSTRecordEntry.value_type_funcs.has_key(val_type):
            func = PSTRecordEntry.value_type_funcs[val_type]
            return func(self.record_entry)
        
        return hex(val_type)
    
def main(args):
    pff_file = pypff.file()
    pff_file.open(args.pst_file)

    root_folder = pff_file.get_root_folder()

    outlook = root_folder.get_sub_folder(OUTLOOK_DATA_FILE)
    inbox = outlook.get_sub_folder(INBOX)
    deleted = outlook.get_sub_folder(DELETED)
    inbox_number_of_messages = inbox.get_number_of_sub_messages()
    deleted_number_of_messages = deleted.get_number_of_sub_messages()

    print "[*] message count"
    print "[inbox] => %d" % inbox_number_of_messages
    print "[deleted] => %d" % deleted_number_of_messages

    if args.details:
        output = sys.stdout
        if args.output is not None:
            output = open(args.output, "w")
        
        try:
            msg = inbox.get_sub_message(args.details)
            sender = msg.get_sender_name()
            subject = msg.get_subject()
            attachments = msg.get_number_of_attachments()
            rs = msg.get_record_set(0)
        
            body = msg.get_plain_text_body()
            
            if attachments > 0:
                output.write("!")
    
            if subject is not None:
                output.write("[%s]" % subject.encode(errors="replace"))
            else:
                output.write("[no subject]")
    
            if sender is not None:
                output.write(" (%s) " % sender.encode(errors="replace"))
            
            output.write(os.linesep)
            
            if body is not None:
                output.write(body)
                output.write(os.linesep)
            
            for entry_index in range(0, rs.get_number_of_entries()):
                entry = PSTRecordEntry(rs.get_entry(entry_index))
                output.write("[%s] => %s" % (unicode(entry.get_type()).encode("utf-8", errors="replace"), unicode(entry.get_value()).encode("utf-8", errors="replace")))
                output.write(os.linesep) 
        finally:
            output.close()
        
    if args.query is not None:
        found = 0
        for index in range(0, inbox_number_of_messages):
            msg = inbox.get_sub_message(index)
            sender = msg.get_sender_name()
            subject = msg.get_subject()
            attachments = msg.get_number_of_attachments()
            rs = msg.get_record_set(0)
            
            body = msg.get_plain_text_body()
                
            if body is not None and args.query in body:
                print "[+] message: %d" % index, 
                                
                if attachments > 0:
                    print "!",
        
                if subject is not None:
                    print u"[%s]" % subject.encode(errors="replace"),
                else:
                    print "[no subject]",
        
                if sender is not None:
                    print u" (%s) " % sender.encode(errors="replace")
                
                found += 1
            
        print "[*] Messages with query found: %d" % found
        
    pff_file.close()

if __name__ == "__main__":
    
    parser = ArgumentParser("PST parser")
    parser.add_argument("pst_file", help="PST file to parse")
    parser.add_argument("-q", "--query", help="query string to search for in body")
    parser.add_argument("-d", "--details", help="index of message to show details for", type=int)
    parser.add_argument("-o", "--output", help="output file to write results to, otherwise uses stdout", type=str)
    
    args = parser.parse_args()
    main(args)