# SessionPlanner-Discord-bot
### $vote
**Params**:
- -from *\<date>* (optional | default: *tomorrow*)
- -to *\<date, included>* (optional | default: *tomorrow + 7 days*)  
**Example**: *$vote -form 21.11.2023 -to 28.11.2023*

### $plan
**Params**
- -date *\<date>* (mandatory)
- -name *\<title of the session>* (optional | default: *Next session*)
- -place *\<place of the session>* (optional | default: *Somewhere*)   
**Example**: *$plan -date 22.11.2023 -name DnD -place "My favourite pub"*

### Notes:
- Date has to follow the dd.mm.yyyy format and cannot include white spaces, e.g. 21.11.2023 or 01.01.2023.
- If white spaces are present in the parameter value, quotation marks have to be used, e.g. "My favourite pub".
- One dash (-) instead of two (--) is used because two dashes are connected to one long dash if used on mobile phone.