Feature: Create School Supply Purchase Checklist
As a SupplyHero user
I want to create a checklist of school supplies from a school supply list
So that I can use it as a checklist to use when purchasing

  Scenario: Create School Supply Purchase Checklist (Normal Flow)
    Given user is logged on
    And user has a school supply list
     When user requests a school supply purchase checklist
     Then a new checklist is created with checkboxes next to each item

  Scenario: Create School Supply Purchase Checklist With No School Supply List (Error Flow)
    Given user is logged on
    And user does not have a school supply list
     When user requests a school supply purchase checklist
     Then "No file has been uploaded." message is shown


