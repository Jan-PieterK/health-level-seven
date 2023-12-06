*** Settings ***
Library  Browser

*** Variables ***
${env}    prod
&{URL}    test=http://localhost:8000/    prod=https://healthlevelseven.com/
${HL7_MESSAGE}    MSH|^~\\&|EPIC|EPICADT|SMS|SMSADT|199912271408|CHARRIS|ADT^A04|1817457|D|2.5|
${expected_HL7_message}       MSH|^~\\&|Test|Test-ORM|Gekoppeld|Tesr|||ORL^O22^ORL_O22|||||||||8859/1\n
${CVS_message}    MSH;1;|\nMSH;2;^~\&\nMSH;3;Test\nMSH;4;Test-ORM\nMSH;5;Gekoppeld\nMSH;6;Tesr\nMSH;9;ORL^O22^ORL_O22\nMSH;18;8859/1
${CSV_FILE}       ${CURDIR}/HL7converter.csv
${EXCEL_FILE}     ${CURDIR}/HL7converter.xlsx


*** Keywords ***
Open HL7
    Browser.Open Browser   ${URL.${env}}   chromium    headless=True

Fill In HL7 Message
    Fill Text    id=text_input    ${HL7_MESSAGE}

Fill In CSV Message
	    Fill Text    id=text_input    ${CVS_message}

Convert
    Browser.Click With Options    id=convert-button    clickCount=1


Verify Convert
    Wait For Elements State    id=copy-button   enabled    timeout=2s

Close Browsers
    Close Browser

Verify Document Is Downloaded
    Promise To Wait For Download    timeout=2s

Upload CSV File
	${promise}=    Promise To Upload File    ${CSV_FILE}
	Click    id=csv_file
    ${upload_result}=    Wait For    ${promise}
    Click With Options    id=upload-button    clickCount=1

Upload Excel File
    ${promise}=    Promise To Upload File   ${EXCEL_FILE}
    Click    id=excel_file
    ${upload_result}=    Wait For    ${promise}
    Click With Options    id=upload-button    clickCount=1

Verify HL7 Message
	Get Text    id=hl7-message    Should Be    ${expected_HL7_message}

*** Test Cases ***
HL7_To_CSV
	Open HL7
	Go To    ${URL.${env}}hl7-to-csv/
    Fill In HL7 Message
    Convert
    Verify Convert
    Close Browsers

HL7_To_Excell
    Open HL7
    Go To  ${URL.${env}}hl7-to-excel/
    Fill In HL7 Message
    Convert
    Verify Document Is Downloaded
    Close Browsers

CSV_To_HL7
    Open HL7
    GO To  ${URL.${env}}/csv-to-hl7/
    Upload CSV File
    Verify HL7 Message

Text_To_HL7
    Open HL7
    GO To  ${URL.${env}}/text-to-hl7/
    Fill In CSV Message
    Convert
    Verify Convert

Excel_To_HL7
    Open HL7
    Go To  ${URL.${env}}excel-to-hl7/
    Upload Excel File
    Verify HL7 Message

