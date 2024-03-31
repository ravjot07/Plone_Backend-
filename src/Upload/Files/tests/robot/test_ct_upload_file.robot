# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s Upload.Files -t test_upload_file.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src Upload.Files.testing.UPLOAD_FILES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/Upload/Files/tests/robot/test_upload_file.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Upload File
  Given a logged-in site administrator
    and an add Upload File form
   When I type 'My Upload File' into the title field
    and I submit the form
   Then a Upload File with the title 'My Upload File' has been created

Scenario: As a site administrator I can view a Upload File
  Given a logged-in site administrator
    and a Upload File 'My Upload File'
   When I go to the Upload File view
   Then I can see the Upload File title 'My Upload File'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Upload File form
  Go To  ${PLONE_URL}/++add++Upload File

a Upload File 'My Upload File'
  Create content  type=Upload File  id=my-upload_file  title=My Upload File

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Upload File view
  Go To  ${PLONE_URL}/my-upload_file
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Upload File with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Upload File title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
