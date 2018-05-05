from IPython.display import Image
from IPython.display import display, Markdown
import change_rating
#PATH VARIABLE FOR IMAGE FOLDER
goto_label=False
def show_book_details(user,book):
    choice_1=0
    #print(book.values)
    print('title : '+str(book['title']))
    path = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python36-32\\programs\\recommendation\\Images\\"
    path = path + str(book['book_id']) + '.jpg'
    #print(path)
    image = Image(path,width = 300,height = 300)

    display(image)
    #Image(image,width = 1000,height = 600)
    print('Author name : '+str(book['authors']))
    print('Publication year : '+str(book['original_publication_year']))
    print('Language of book : '+str(book['language_code']))
    print('Average rating : '+str(book['average_rating']))
    #print()
    click_reward=1
    final_reward=click_reward
    dislike_reward=-2
    like_reward=2
    while(choice_1!=4):
        print('1. Like\n2. Dislike\n3. Rate\n4. Back')
        choice_1 = int(input('Choose an option : '))
        switcher_1 = {
            1: "Like",
            2: "Dislike",
            3: "Rate",
            4: "Back"
        }
        choice_1_output = switcher_1.get(choice_1)
        if(choice_1_output == "Like"):
            print(choice_1_output)
            #add reward
            final_reward+=like_reward
        elif(choice_1_output == "Dislike"):
            print(choice_1_output)
            #add penalty
            final_reward+=dislike_reward
        elif(choice_1_output == "Rate"):
            print(choice_1_output)
            rating=int(input("Enter rating between 1 to 5 : "))

            ch_rate=change_rating.change_rating
            ch_rate(user,book['book_id'],rating)
            if(rating>3):
                rate_reward=4
            else:
                if(rating>=2):
                    rate_reward=3
                else:
                    rate_reward=2
            final_reward+=rate_reward
            print(rating)
            #save rating
        elif(choice_1_output == "Back"):
            #print(choice_1_output)
            goto_label=True
        else:
            print('Wrong Choice')
    return final_reward
