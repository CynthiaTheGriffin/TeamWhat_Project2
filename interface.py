import psycopg2

### 1: Add a new player
def register_player():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()
        
    # Prompts
    id = input("Enter a new 5-character ID: ")
    name = input("Enter player name: ")

    try:
        query = '''
        INSERT INTO player VALUES (%s,%s)
        ;'''
        cur.execute(query, (id, name))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        print("ID already in use.\n")
        conn.rollback()
    except psycopg2.errors.CheckViolation:
        print("Invalid ID. It must be 5 characters long.\n")
        conn.rollback()
    except psycopg2.Error as e:
        print("Other Error")
        print(e)
        conn.rollback()

    conn.close()
    return


### Find the current balance of a player
def __get_balance(player_id):
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    query = '''
    SELECT SUM(amount)
    FROM credit_history
    WHERE player_id LIKE %s
    ;'''
    cur.execute(query, (player_id,))

    balance = cur.fetchone()[0]
    conn.close()
    return balance


### 2: Add to the credit balance of a player
def add_balance():

    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    # Prompts
    id = input("Enter player ID: ")
    amount = input("Enter the player's change in balance (do not use '+' sign): ")

    try: 
        if float(amount) <= 0:
            print("Please enter a positive value.\n")
            conn.close()
            return
    except ValueError:
        print("Please enter a numerical value.\n")
        conn.close()
        return

    try:
        query = '''
        INSERT INTO credit_history VALUES (%s, CURRENT_TIMESTAMP,%s)
        ;'''
        cur.execute(query, (id, amount))
        conn.commit()
        conn.close()
    except psycopg2.errors.ForeignKeyViolation:
        print("The given player ID does not exist.\n")
        conn.rollback()
        conn.close()
        return
    except psycopg2.errors.NumericValueOutOfRange:
        print("Balance too large.")
        conn.rollback()
        conn.close()
        return
    except psycopg2.Error as e:
        print("Other Error")
        print(e)
        conn.rollback()
        conn.close()
        return        

    balance = __get_balance(id)
    print(f"Current balance: {balance}")

    conn.close()
    return


### 3: Update play history and credit balance when a player plays a game
def play_game():

    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    # Prompts
    player_id = input("Enter player ID: ")
    machine_id = input("Enter machine ID: ")
    
    game_query = '''
    SELECT cost
    FROM machine NATURAL JOIN game
    WHERE machine_id = %s
    ;'''
    
    cur.execute(game_query, (machine_id,))
        
    result = cur.fetchone()
    if result is None:
        print('Machine ID not found.')
        conn.close()
        return
    game_cost = result[0]

    player_balance = __get_balance(player_id)
    if player_balance is None:
        print("Player ID not found.")
        return
    
    if (float(game_cost) > float(player_balance)):
        print("Insufficient funds")
        conn.close()
        return
    
    score = input("Enter player score: ")
    
    try:
        insertion_query = '''
        INSERT INTO play_history VALUES (%s, CURRENT_TIMESTAMP, %s, %s);
        INSERT INTO credit_history VALUES (%s, CURRENT_TIMESTAMP, %s)
        ;'''
        cur.execute(insertion_query, (machine_id, player_id, score, player_id, -1*game_cost))
        conn.commit()
    except psycopg2.Error as e:
        print("Other Error")
        print(e)
        conn.rollback()

    conn.close()
    return 


### 4: Display the credit history of a player
def show_credit_history():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    # Prompts
    id = input("Enter player ID: ")

    query = '''
    SELECT *
    FROM credit_history
    WHERE player_id LIKE %s
    ORDER BY time_stamp
    ;'''
    
    cur.execute(query, (id,))
    
    # Print results
    for _, time_stamp, amount in cur:  
        print(f"{time_stamp} -- {amount}")

    conn.close()
    return


### 5: Display the purchase history of a player
def show_purchase_history():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    # Prompts
    id = input("Enter player ID: ")

    query = '''
    SELECT *
    FROM purchase_history
    JOIN prize USING(prize_id)
    WHERE player_id LIKE %s
    ORDER BY time_stamp
    ;'''
    cur.execute(query, (id,))
    
    # Print results
    for _, _, time_stamp, quantity, prize_name, cost in cur:  
        print(f"{time_stamp}\t {prize_name} ({quantity}): {cost*quantity} tickets")

    conn.close()
    return


### 6: Display the play history of a player
def show_player_play_history():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    id = input ("Enter player ID: ")

    player_query = '''
    SELECT player_name
    FROM player
    WHERE player_id LIKE %s
    ;'''
    cur.execute(player_query, (id,))
    temp_output = cur.fetchone()
    if temp_output == None:
        print("Player ID not found.")
        conn.close()
        return
        
    player_name = temp_output[0]

    history_query = '''
    SELECT game_name, score, time_stamp
    FROM play_history NATURAL JOIN machine NATURAL JOIN game
    WHERE player_id LIKE %s
    ORDER BY time_stamp
    ;'''

    cur.execute(history_query, (id,))

    # Print results
    print(f"Play history for {player_name}")
    for game_name, score, time_stamp in cur:  
        print(f"{game_name}\t {score}\t {time_stamp}")

    conn.close()
    return

### 7: Display the play history of a machine (not game)
def show_machine_play_history():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    id = input ("Enter machine ID: ")

    game_query = '''
    SELECT game_name
    FROM machine NATURAL JOIN game
    WHERE machine_id LIKE %s
    ;'''
    cur.execute(game_query, (id,))
    temp_output = cur.fetchone()
    if temp_output is None:
        print("Machine ID not found.")
        conn.close()
        return
    
    game_name = temp_output[0]

    history_query = '''
    SELECT player_id, score, time_stamp
    FROM play_history
    WHERE machine_id LIKE %s
    ORDER BY time_stamp
    ;'''

    cur.execute(history_query, (id,))

    # Print results
    print(f"Play history for {id} ({game_name})")
    for player_id, score, time_stamp in cur:  
        print(f"{player_id}\t {score}\t {time_stamp}")

### 8: Display personal high scores for a player
def show_personal_scores():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    id = input ("Enter player ID: ")

    player_query = '''
    SELECT player_name
    FROM player
    WHERE player_id LIKE %s
    ;'''
    cur.execute(player_query, (id,))
    temp_output = cur.fetchone()
    if temp_output == None:
        print("Player ID not found.")
        conn.close()
        return
    
    player_name = temp_output[0]

    history_query = '''
    SELECT game_id, game_name, score, time_stamp
    FROM play_history NATURAL JOIN machine NATURAL JOIN game
    WHERE player_id LIKE %s
    ORDER BY time_stamp
    ;'''

    cur.execute(history_query, (id,))

    high_scores = {}

    for game_id, game_name, score, time_stamp in cur:
        if game_id not in high_scores.keys():
            high_scores.update({game_id:(game_name,score,time_stamp)})
        else:
            if int(score) > int(high_scores.get(game_id)[1]):
                high_scores.update({game_id:(game_name,score,time_stamp)})

    # Print results
    print(f"High scores for: {player_name}\n")
    print("Game\tScore\tTimestamp")
    for high_score in high_scores.items():
        data = high_score[1]
        print(f"{data[0]}\t{data[1]}\t{data[2]}")
    
    conn.close()
    return
    
### 9: Display local high scores for the establishment
def show_local_scores():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    history_query = '''
    SELECT game_id, game_name, player_name, score, time_stamp
    FROM play_history NATURAL JOIN machine NATURAL JOIN game NATURAL JOIN player
    ORDER BY time_stamp
    ;'''

    cur.execute(history_query)

    high_scores = {}

    for game_id, game_name, player_name, score, time_stamp in cur:
        if game_id not in high_scores.keys():
            high_scores.update({game_id:(game_name,player_name,score,time_stamp)})
        else:
            if score > high_scores.get(game_id)[1]:
                high_scores.update({game_id:(game_name,player_name,score,time_stamp)})

    # Print results
    print(f"High scores\n")
    for high_score in high_scores.items():
        data = high_score[1]
        print(f"Game: {data[0]}")
        print(f"{data[1]}\t{data[2]}\t{data[3]}\n")
    
    conn.close()
    return

### 10: Update machine status and maintenance history
def update_maintenance():
    
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()
        
    # Prompts
    machine_id = input("Enter machine ID: ")
    employee_id = input("Enter employee ID: ")
    condition = input("Enter updated machine condition: ")
    notes = input("Enter maintenance notes: ")

    try:
        query = '''
        UPDATE machine
        SET condition = %s
        WHERE machine_id LIKE %s
        ;'''
        cur.execute(query, (condition, machine_id))

        query = '''
        INSERT INTO maintenance_history VALUES (%s,%s,CURRENT_TIMESTAMP,%s)
        ;'''
        cur.execute(query, (machine_id, employee_id, notes))
        
        conn.commit()
    except psycopg2.errors.ForeignKeyViolation:
        print("Invalid employee ID or machine ID.\n")
        conn.rollback()
    except psycopg2.errors.CheckViolation:
        print("Invalid condition. Please enter 'running' or 'out of service'.\n")
        conn.rollback()
    except psycopg2.Error as e:
        print("Other Error")
        print(e)
        conn.rollback()

    conn.close()
    return


### 11: Display the conditions of all machines
def show_machines():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    query = '''
    SELECT machine_id, game_name, condition
    FROM machine NATURAL JOIN game
    ;'''

    cur.execute(query)

    # print results
    print("Machine ID (Game)\tStatus")
    for machine_id, game_name, condition in cur:
        print(f"{machine_id} ({game_name})\t{condition}")

    conn.close()
    return

### 12: Display the maintenance history of a machine
def show_maintenance_history():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    machine_id = input("Enter the machine ID: ")

    machine_query = '''
    SELECT game_name, condition
    FROM machine NATURAL JOIN game NATURAL JOIN maintenance_history
    WHERE machine_id LIKE %s
    ;'''

    cur.execute(machine_query, (machine_id,))
    machine_info = cur.fetchone()
    if machine_info == None:
        print("Machine ID not found.")
        conn.close()
        return
    
    # print headers
    print(f"Maintenance History for: {machine_id} ({machine_info[0]})\tStatus: {machine_info[1]}")
    print("Employee Name\tEmployee ID\tTimestamp\tNotes")

    history_query = '''
    SELECT employee_name, employee_id, time_stamp, employee_notes
    FROM maintenance_history NATURAL JOIN employee
    WHERE machine_id LIKE %s
    ORDER BY time_stamp
    ;'''
    cur.execute(history_query, (machine_id,))

    # Print results
    for employee_name, employee_id, timestamp, employee_notes in cur:
        print(f"{employee_name}\t{employee_id}\t{timestamp}\t{employee_notes}")
    
    conn.close()
    return


### 13: Add new purchase to purchse history
def add_purchase():
    # Connect to database
    conn = psycopg2.connect(dbname="what")
    cur = conn.cursor()

    player_id = input("Enter player ID: ")
    prize_id = input("Enter prize ID: ")
    quantity = input("Enter quantity of the prize: ")
    
    try:
        query = '''
        INSERT INTO purchase_history VALUES(%s,CURRENT_TIMESTAMP,%s,%s)
        '''
        cur.execute(query, (player_id, prize_id, quantity))
        conn.commit()
    except psycopg2.errors.ForeignKeyViolation:
        print("Invalid player ID or prize ID.")
        conn.rollback()
    except psycopg2.errors.NumericValueOutOfRange:
        print("Quantity too large.")
        conn.rollback()
    except psycopg2.errors.CheckViolation:
        print("Quantity must be 1 or greater.")
        conn.rollback()
    except psycopg2.Error as e:
        print("Other Error")
        print(e)
        conn.rollback()

    conn.close()
    return


terminated = False
while (not terminated):
    # List all possible actions
    print("What action would you like to take?")
    print("\t--Input 1 to register a new player")
    print("\t--Input 2 to add money to a player's account")
    print("\t--Input 3 to update play records")
    print("\t--Input 4 to generate a player's credit history")
    print("\t--Input 5 to generate a player's purchase history")
    print("\t--Input 6 to generate a player's playing history")
    print("\t--Input 7 to generate a machine's playing history")
    print("\t--Input 8 to generate a player's personal high scores")
    print("\t--Input 9 to generate the leaderboard")
    print("\t--Input 10 to update maintenance records")
    print("\t--Input 11 to check the status of all machines")
    print("\t--Input 12 to generate maintenance records")
    print("\t--Input 13 to update purchase records")
    action = input("Please input a number to indicate your selection: ")
    action = action.strip()

    if action == '1':
        register_player()
    elif action == '2':
        add_balance()
    elif action == '3':
        play_game()
    elif action == '4':
        show_credit_history()
    elif action == '5':
        show_purchase_history()
    elif action == '6':
        show_player_play_history()
    elif action == '7':
        show_machine_play_history()
    elif action == '8':
        show_personal_scores()
    elif action == '9':
        show_local_scores()
    elif action == '10':
        update_maintenance()
    elif action == '11':
        show_machines()
    elif action == '12':
        show_maintenance_history()
    elif action == '13':
        add_purchase()
    elif action in ['exit', 'Exit', 'e', 'quit', 'Quit', 'q']:
        terminated = True
    else:
        print("Invalid selection. Please enter a single integer from 1 to 9.")