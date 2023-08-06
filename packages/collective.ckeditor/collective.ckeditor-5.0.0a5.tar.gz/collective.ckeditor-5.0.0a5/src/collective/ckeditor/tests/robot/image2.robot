*** Settings ***

Library  collective.ckeditor.tests.keyword.TestKeywords

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Test Setup  Open test browser
Test Teardown  Run keywords  Close all browsers

*** Variables ***

${SELENIUM_IMPLICIT_WAIT}  2

*** Test cases ***

Scenario: Uses image2 editor
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor uses image2 editor
    Click element  css=.cke_dialog_ui_button_cancel
    Cancel edit

*** Keywords *****************************************************************

# --- GIVEN ------------------------------------------------------------------

a logged-in editor
  Enable autologin as  Editor  Contributor

a document
  Create content  type=Document  id=document-to-edit  title=Document to edit  text=<p id="p1">paragraph1</p><p id="p2">paragraph2</p><p>paragraph3</p><p>paragraph4</p>
  Go to  ${PLONE_URL}/document-to-edit
  Page Should Contain  paragraph1
  Page Should Contain  paragraph4
  Page Should Contain Element  css=#p1
  Page Should Not Contain Element  css=#p1 strong

# --- WHEN -------------------------------------------------------------------

I edit the document
  Go to  ${PLONE_URL}/document-to-edit/edit

# --- THEN -------------------------------------------------------------------

CKEditor uses image2 editor
  Page Should Not Contain Element  css=.cke_editor_form_widgets_IRichTextBehavior_text_dialog .cke_dialog_title
  Page Should Contain Element  css=a.cke_button__image
  Wait Until Element Is Visible  css=a.cke_button__image
  # Use javascript instead of selenium that fails on Github
  #
  # Click link  css=a.cke_button__image
  Execute javascript  document.querySelector('a.cke_button__image').click();
  Wait Until Element Is Visible  css=.cke_editor_form_widgets_IRichTextBehavior_text_dialog .cke_dialog_title
  Page Should Contain Element  css=.cke_editor_form_widgets_IRichTextBehavior_text_dialog .cke_dialog_title
  Element should contain  css=.cke_editor_form_widgets_IRichTextBehavior_text_dialog .cke_dialog_title  Image Properties
  Element should contain  css=.cke_editor_form_widgets_IRichTextBehavior_text_dialog  Captioned image

Cancel edit
  Unselect frame
  Execute javascript  document.querySelector('.formControls').scrollIntoView(true);
  Set focus to element  name=form.buttons.cancel
  Sleep  0.5
  Backport Wait For Then Click element  name=form.buttons.cancel

Backport Wait For Element
    [Documentation]  Can contain css=, jquery=, or any other element selector.
    ...              Element must match exactly one time.
    [Arguments]  ${element}
    Wait Until Page Contains Element  ${element}
    Set Focus To Element  ${element}
    Wait Until Element Is Visible  ${element}
    Sleep  0.1
    ${count} =  Get Element Count  ${element}
    Should Be Equal as Numbers  ${count}  1

Backport Wait For Then Click Element
    [Documentation]  Can contain css=, jquery=, or any other element selector.
    ...              Element must match exactly one time.
    [Arguments]  ${element}
    Backport Wait For Element  ${element}
    Click Element  ${element}
