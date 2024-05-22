import requests
from pprint import pprint
from tqdm import tqdm
import random
import pandas as pd
import matplotlib.pyplot as plt

# List of project rows will be stored in this
projects = []
possible_headers = [
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
]
current_viewstate = "scSllP3FYjNW12aUazc9H2DqCp%2FQlAbLk8JKE5ddwZP8A0kW2FDOJZ35pJbI%2FvIfNGaSa0%2BkZ%2Byw8erC1O3dlK0O99tY%2FyYLG%2BYQPq5VrjP0vc44bFTt%2FwQ1z74d62nALigvyN8CsR3LT5VAoezunKqECIoi19f4tsCjJeJfPFxlOJPhlIcKiTXt7%2BZNvgjIFUs78xngpgh2rFwmAwwsn3CoSav8w5hhzNpcGC45iKI%2FKmSdzy1LteoHytimKTc11UbbeVt1CjHEVNIoXxWdPtNY72Af9XOq%2BpiaLepzZgYtQX67PCC1hCJCxPjTYNcHNiIvLk6wfXNjoHI1izMCCHWJPzTW6ENUSzBzcWWwYhMGRv%2FbTPGEOjHQY8fYVzn2NdrAK2k%2FLs1xde8LSW9S3d7R%2F8WuoIHlF4RuOabMP2AD2zRvwaJsQ4ZCyUDdI%2BwSqS%2B05y8%2FyWTxevh4Ldamv2zZJVEj5x1d08BVSVPicRtyrKc8JlViAFr%2FV1FiGRbNrN037Rv3svQYyFp0PyWJpGvKK2d6RDdFkHrUbRBbMhTH3D9Za6DjnAQ4Ngi4TN%2BT82pSxQKsLN5hydQyeBTk9oZStASsS5mFDjtcWWgt4DtnZhihJ%2BbTzxc8cVxHEH739MuMdl%2BGv5nBU7qZYrdsrWIx7%2FGkwdXPmpiP26oOO3j76Yomr%2BdgMzf5bwgDAIJeCxs0CnO2HtOxmrR92d1otQ%3D%3D"
current_validation = "y8vnE0j3n4hGnfyMLccq1W%2B%2BaYXuCJ9AtpIcUDkTx5N%2F0V%2FtLIBqmdpiOwJcsme5uIafxdSoC%2FBH8J8VnhZ3LnrSuZIwhjG736ZGwROmD4DjPYIDhT5MT6eBrqPgxoxki70zNvd1eb3ieQ7pBCbKPdYW2yH3xLRBh5kG%2BtIDZ7bi6BWHk639aG2%2FoXoMZrP2KgsjaYyjRPNuGHYjGcpu9%2B1kj%2BCZqUBDChHTVQB5ipAOygprejzoySO6KC%2BphFk7veuhUQPkWzScppvKpLPfs%2B80qufWKP2KWJskDsUFbng%3D"
# current_viewstate = "MQuJPJ%2Bbq84%2BiSst5QB8%2F%2B9%2B3DQJYW%2FQZ%2BGmLHq1lxFYyNsOYDt59kUS%2Bri%2FZSZGCQRB%2Fe4e7AN%2BDmolpSM%2BbmVdell%2FfuJJlBr4KqqCWWn6hdRmUQ5Mtfw0%2BotGBHluBszagVwLrewOvmca43DzrKsZIyqKBDO5qpjI71aeC6wNQPRC7DgmbwrdfU5I56QrCmMZ39XN8fXT9IZQJ60Gdf%2BNO6RkmNxklb%2BrEf4nFRYLh1WQcWey3v1u3yrzd%2Bj4M0%2Fxiqo%2BieDMnm96sie0i3LigHg0umeQfbq3Y511Ai2MWAPSQZ106vHMAmMmAimvBTety2RPO3iGR8fibLIjSvG4cfZZj0HtG77emTztDwzCtB5HttqulY2AeG0E4Aaj2PxGDvXs0Bu7LiRCPPssULOIhwi5U7xDTqudqkDoPnsknZEcLeUqJ8PJJwXbPAMJoBthOC7kUszZvLFocT%2FoDR4JEJqXuc9%2BamXvz2qZOP4ar4lDH7EV6xQnxd2Ehj4IpbHlVd9db3ZACAg60XF0qPLHwY1%2FXtD%2BsnNjuhImxnW%2BC4UOA21W9Kbq0PVtn8SJH1JwRwVi38PPbNshLMrUTfwojh4%2BhWinbKSXMFY5g0yfbXp%2BUCs%2B1HdFYlH9nYyg%2FFb8CqI6o55JapHRzoWjS4Q4EuVwmz7VSS0CX%2BvFA51A8VlgFlHLR5dOfgm4LEaISKcui%2FoRH6L%2BWrs7qvpPWeIQWmfTos%2B%2FeM5%2B4FodsCZefuix09jo3mLfPmXTeW4z%2BXZPvq9okjwFMf6rTkGvc52yCRxccYyFKCToyG3w3OWMcZQTB%2FmOuiLcD51aIb7ER3aFrCUeiJwrrAAX15GDonfn9ZaGZGjTyzrgpx%2F%2F4QSxXqye7V8mfpgFhkSWV4ZHyAz9EEl6yTa0%2FTUJd3sfvxmGAmHUMeJ6Dn7U%2BbvDIwB60Ezuv9R32Vztr%2BHHOXD%2F7%2B9MSZkpQv0Ob9cjOiA5SP8ZYRSSC5kxsI0NNaYeP9dWZR%2BTloz0L%2BY2aZYsBdf8syK9DCYJPh2g%2FXrTIDtHp%2FbWBenGI2UUPc%2BfR2nUOtNQH30I3dmoO55o2Eb4ST52rPOQEU1W0Egh%2Fvd2iMcOkYgkH4aajZWK8bWw4QgvgpWZV%2Fn7lHpgSvGYpzCYAPPhqXj8tz2mk7Ws%2Bp%2FtzGmsbAHNBp%2BmJ%2BiMNwUdtzBHC%2BVg3Bc4dNdHjfkM7p18wOolCMKtYSdv9uN2RWY0pfLDI6obEKH6lAoLwcSow64%2BiDBEkq8FnlC2lyDX10sVLebrh7OgfMv1xMix46Bt8mBh4JqCdXZR9EVRhl3kjxJy%2FBpEZVplVft7YC6meJ0bnp%2BTqFTPUV0KpJHyxXfCgtjL5ZVoD%2FaDuG4iyilTEWm7jdlysUtxqYnOHmZpJ0IKPMOKITGUUNSGmhDFkBWjSpcc9JG6xfzNS6T74X3%2BdK3bXtMGMuufT%2Bk96d8a%2B2WNti58Ie96C0WVaUvBepz8CU87d4iMLgKww3Vx5VET3mpbmbpbpcVUVlXZeBMSns%2Fzod1PXRQ7YThqM%2FTxt4Sa%2FH8nlgefm5vgzq7sRAuqxr%2BP8cYrdt5mlkNqB%2F6TIQwKpzhaRvJRcAiuLOQoPsya%2FFdkJtTBXWdp43bshdhBOb1KCdxJejsbccXEQy7SA7lhc32nxqetOimKlOkODugUOcAWPCxZ2XD%2BgrIN8dmBZnsZJMq1q2igx575RV%2F4RBaagJzg2NUUei26vYx6XKOOTJa4BF1bmTKJzQWJmcNddeJMlVScSvQ374We9%2Fs44066gfo6%2F0G33plAcQ%2FION3YTVWr2kfYOaPSsVAQ46%2Fw0imuSjxNG8HSYNy9ama5IOas%2BgAFp0PSmOphX6%2FYxpdUjnoPoo9j26e%2FIomuYar9EKoGiBzxuukEP3AtP8NtNc1xDDI7l5GMzDjmqsE%2BhSCOMgOzgGQN%2Fw0IbYmRo4e%2BHQLj8bpHcjh4y80Eucs9Fn3IXZBMoAgogBinAwkd%2F1g67%2FnFuER8RBmCXshQU7c7qThLOhh7o4ljeo55j%2FYyII%2Brx6wqTo5wMOWLUBSVNnjV7ujDfVNHfRSAcJpvo%2FFOLcGCDn1JKCBEOAgCOKRdsfi3dXpojIkQO9nf83HO%2FLo10GcJAGCmhbhiqAwir0vn0Egb33vASN0eRO5fKX1SWNCwiwo%2BWJlrr93KU3C%2B6aIVDRPU9DURgH6uY%2Fn18asPn3fOphq9ZOZkdum11N7z%2FKuz3LgR2z0U9WFYQ6JRiQyrqUPywoX4mxrGNmpZxjrDWMP5iaMFn05n%2BpqZqOT45HoEcD3rZCbEzUmKodXcGJ68mBQlwQOhQ6b3g4%2FmRLPFTbcTXfXcXkBubmw%2B7Mfp9r5YDMOICGLdHT37TDQqUFcNep2LVRiGwNvF3lyqyzoS45BTFxSUccuuYU8K0Kfpr6VmrS%2BZ%2Fnba8BpETbXVwvegGAWUE9k3SH8B%2BSCYAA9VDgIlJ%2F71Qa3JU0Kbkp0GxPQaOKx7ngR4GGadHqbn8wzJkicCTw%3D%3D"
# current_validation = "%2BhFaCIH0MItOGHmY5RG%2B0%2BN%2BhnVz79bxMkrKSoDgTSuX3GWPUiTndWZvKADIsckM65P2MQS9cPEhs6NQUf0XmDmtB4CT7M23qUPW4W%2Fm01pU7FM0v5Npv4BWeqyVzMwOxwLL9f%2FGwMK4owhqzy9Hph%2FcIuh1LJMF9AB8ThJuERFfArqxaGvkAHBuFHWjlr4WdZODbk1xbgjFBfISjsbgAfuh41R2AySTAD07VVvFnPA%2B4oQ2CIMcthiqByCVi3BHWaMKXdgnTelK12ffLVk3KohHsa7M6ezGxj8bUO5nKLWp2cK8%2F8KAA4nNaGwaVG2KmXpPY3W7oh1fCu6F%2BhPPGsv5pSV67wNYjlt3PRVY56Yk%2FZPaBkSkXjfoiav22h4c"


# Send a request as the frontend asking for one html page worth of data
def grab_project_numbers(session, state_name, page_number, key):
    global current_viewstate, current_validation
    base_url = "https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename="
    url = base_url + state_name

    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://environmentclearance.nic.in",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": url,
        "Cookie": "ASP.NET_SessionId = 0czkxyx411fdbinxpsfxpi3c; acopendivids = Email, Campa, support, livestat, commitee, Links; acgroupswithpersist = nada",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
    }

    # Payload data which determines what information they'll send back
    event_target = "ctl00%24ContentPlaceHolder1%24grdevents"
    event_argument = f"Page%24{page_number}"
    search_argument = f"{key}"
    state_name_argument = f"{state_name.replace(' ', '+')}"
    post_data = f"__EVENTTARGET={event_target}&__EVENTARGUMENT={event_argument}&__VIEWSTATE={current_viewstate}&__VIEWSTATEGENERATOR=AAD58642&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION={current_validation}&ctl00%24ContentPlaceHolder1%24RadioButtonList1=EC&ctl00%24ContentPlaceHolder1%24textbox2={search_argument}&ctl00%24ContentPlaceHolder1%24btn=Search&ctl00%24ContentPlaceHolder1%24HiddenField1={state_name_argument}"

    # Try sending the request and report if there is an error
    try:
        response = session.post(url, data=post_data, headers=headers)

        if response.status_code == 200:
            # note that parse_project_numbers_html must be called immediately afterwards so that the viewstate value
            # can be extracted from this response html and updated in the global variable current_viewstate
            current_viewstate = response.text.split('id="__VIEWSTATE" value="')[1].split('" />')[0].replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")
            current_validation = response.text.split('id="__EVENTVALIDATION" value="')[1].split('" />')[0].replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")

            post_data = f"__EVENTTARGET={event_target + '%24ctl02%24lnkDelete'}&__EVENTARGUMENT={event_argument}&__VIEWSTATE={current_viewstate}&__VIEWSTATEGENERATOR=AAD58642&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION={current_validation}&ctl00%24ContentPlaceHolder1%24RadioButtonList1=EC&ctl00%24ContentPlaceHolder1%24textbox2={search_argument}&ctl00%24ContentPlaceHolder1%24btn=Search&ctl00%24ContentPlaceHolder1%24HiddenField1={state_name_argument}"
            smth = session.post(url, data=post_data, headers=headers)
            if "pid=" in smth.text and "pid=C" not in smth.text:
                print(smth.text)

            return response.text
        else:
            print(f"Error: {response.status_code}")
            return

    except Exception as e:
        print(f"An error occurred: {e}")


# Convert the html into one row of data per project
def parse_project_numbers_html(html_page):
    projects_data = []

    # Parse the fifth table in the page
    # The "try" catches the case when a NoneType object has been returned
    try:
        table = html_page.split("<table")[5 * 2 + 1]
        rows = table.split("<tr")[1 * 2:]
    except AttributeError as e:
        return projects_data

    for row in rows[:10]:
        projects_data.append([])
        cells = row.split("</td>")

        # For each project, try to parse the html row
        for cell in cells[:-2]:

            try:
                stripped_cell = cell.strip().replace("\n", "").strip().replace("\r", "").strip()
                if not projects_data[-1]:
                    # projects_data[-1].append(((page_number-1)*10) + int(stripped_cell.split(">")[-1].strip()))
                    projects_data[-1].append(int(stripped_cell.split(">")[-1].strip()))
                else:
                    projects_data[-1].append(stripped_cell.split('">')[2].split("</span>")[0])
            except Exception as e:
                print("Error in parsing:", e)
                print(stripped_cell)

    return projects_data


def area_chart(sequence):
    plt.fill_between(range(len(sequence)), sequence, color="skyblue", alpha=0.4)
    plt.plot(sequence, color="Slateblue", alpha=0.6, linewidth=2)

    # Add labels and title
    plt.xlabel("Iteration")
    plt.ylabel("Projects")
    plt.title("Total project count over time")

    # Show the plot
    plt.show()


# Construct the table of projects
def grab_list_of_projects(session, state_name, pages, key):
    # set variables for this run
    global projects
    page = 1
    collision_count = 0
    more_pages_exist = True
    project_counts = []

    pbar = tqdm(total=pages)
    while more_pages_exist:

        # grab and parse the page
        response = (grab_project_numbers(session, state_name, page % 20, key))
        new_projects = parse_project_numbers_html(response)

        # check for collisions
        for new_project in new_projects:
            if new_project[1] in [x[1] for x in projects]:
                collision_count += 1
            else:
                projects.append(new_project)

        # end the loop
        if page >= pages - 1:
            more_pages_exist = False
            pbar.close()
        else:
            page += 1
            pbar.update(1)

        project_counts.append(len(projects))

    # Expected collision rate is about 50% for the three-digit total pages range
    print(f"Found {len(projects)} projects with {collision_count} collisions.")
    area_chart(project_counts)
    # pprint(projects)

    # Return the data as a pandas object
    data = pd.DataFrame(projects,
                        columns=["index", "project_number", "file_number", "project_name", "company", "proposal_status",
                                 "project_type"])
    data.drop(["index"], axis=1, inplace=True)
    return data


if __name__ == "__main__":
    state = "West Bengal"
    filename = f'../{state.replace(" ", "_")}/scraped_projects.csv'

    with requests.Session() as session:

        num_pages = 100
        iteration_count = 14
        keys = [str(x) for x in range(2015, 2024)] + ["IN", "IND", "MIN", "MIS", "20", "WB"]

        df = pd.DataFrame(columns=["index", "project_number", "file_number", "project_name", "company", "proposal_status",
                                   "project_type"])

        for iteration in range(iteration_count):
            data_df = grab_list_of_projects(session, state, num_pages, keys[iteration])
            df = pd.merge(df, data_df, how='outer')
            df = df.drop_duplicates()

        filename = f'../{state.replace(" ", "_")}/scraped_projects.csv'
        df.to_csv(filename, index=True)
