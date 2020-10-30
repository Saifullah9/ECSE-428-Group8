Feature: Display a School Supply List

As a SupplyHero user
I want to request all my school supply lists from the SupplyHero application
So that I can see the school supply lists in my account

	Scenario Outline: Display all School Supply Lists (Normal Flow)
    Given user is logged on
    When user requests all school supply lists
    Then all lists of school supplies are displayed


    Scenario Outline: Display a School Supply List with no Lists (Error Flow)
    Given user is logged on
    When user requests a school supply list
    But there is no list of school supplies
    Then a "You do not have any lists of school supplies." message is shown