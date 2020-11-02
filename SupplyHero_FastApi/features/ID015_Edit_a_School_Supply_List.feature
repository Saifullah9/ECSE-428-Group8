Feature: Edit a School Supply List
As a SupplyHero user
I want to edit a school supply list
So that the new school supply list fits my child's academic needs

  Scenario: Edit a School Supply List (Normal Flow)
    Given user is logged on
    And user has a school supply list's ID
    When user requests to edit a school supply list with its' ID
    Then a new edited school supply list is updated in the user's account
     
  Scenario: Edit a School Supply List with no New Data (Error Flow)
    Given user is logged on
    And user has a school supply list's ID
    When user requests to edit a school supply list with its' ID
    But the content of the school supply list is the same
    Then "The school supply list is the same" message is displayed




