# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s Upload.Files -t test_upload_files.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src Upload.Files.testing.UPLOAD_FILES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/Upload/Files/tests/robot/test_upload_files.robot
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

Scenario: As a site administrator I can add a Upload Files
  Given a logged-in site administrator
    and an add Upload Files form
   When I type 'My Upload Files' into the title field
    and I submit the form
   Then a Upload Files with the title 'My Upload Files' has been created

Scenario: As a site administrator I can view a Upload Files
  Given a logged-in site administrator
    and a Upload Files 'My Upload Files'
   When I go to the Upload Files view
   Then I can see the Upload Files title 'My Upload Files'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Upload Files form
  Go To  ${PLONE_URL}/++add++Upload Files

a Upload Files 'My Upload Files'
  Create content  type=Upload Files  id=my-upload_files  title=My Upload Files

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Upload Files view
  Go To  ${PLONE_URL}/my-upload_files
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Upload Files with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Upload Files title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
