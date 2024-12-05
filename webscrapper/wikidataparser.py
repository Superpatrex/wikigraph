import requests
from bs4 import BeautifulSoup
import urllib.parse
import networkx as nx
import community as community_louvain

LOWER_CASE_STATES = [
    'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 
    'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 
    'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 
    'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 
    'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 
    'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina', 'south dakota', 
    'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 
    'wisconsin', 'wyoming'
]

REMOVED_WORDS = [
'covid-19_pandemic_in',
',_',
'election',
'presidential',
'list_of',
'presidency',
'primary',
'congressional_district',
'district_election',
'mayoral_election',
'gubernatorial_election',
'united_states_congress',
'governor',
'national_convention',
'electoral_history',
'state_of_the_union_address',
'bibliography',
'inauguration',
'special_election',
'electoral_college',
'administration'
]

PRESIDENTS = [
    'Donald Trump', 'Joe Biden', 'Richard Nixon', 'Gerald Ford', 
    'Jimmy Carter', 'Ronald Reagan', 'George H. W. Bush', 
    'Bill Clinton', 'George W. Bush', 'Barack Obama'
]

WIKIPEDIA_URLS = [
    'https://en.wikipedia.org/wiki/1972_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/1976_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/1980_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/1984_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/1988_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/1992_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/1996_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2000_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2004_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2008_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2012_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2016_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2020_United_States_presidential_election',
    'https://en.wikipedia.org/wiki/2024_United_States_presidential_election'
    ]

def get_embedded_links(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        lower_href = href.lower()
        if all(state not in lower_href for state in LOWER_CASE_STATES) and all(state not in lower_href for state in REMOVED_WORDS) and href.startswith('/wiki/') and ':' not in href.split('/wiki/')[1]:
            links.add('https://en.wikipedia.org' + href)

    return list(links)

def get_links_from_multiple_articles(urls):
    all_links = []
    for url in urls:
        links = get_embedded_links(url)
        all_links.append((url, links))
    return all_links

def convert_wikipedia_url_to_text(url):
    return urllib.parse.unquote(url).split('/wiki/')[1].replace('_', ' ')

def run_presidential_election_web_scrapper():
    adjacency_list = {url: [] for url in WIKIPEDIA_URLS}

    url_to_id = {}
    unique_id_counter = 0
    adjacency_list = {}
    incoming_edges_count = {}

    for url in WIKIPEDIA_URLS:
        if url not in url_to_id:
            url_to_id[url] = unique_id_counter
            unique_id_counter += 1
        links = get_embedded_links(url)
        incoming_edges_count[url] = len(links)
        for link in links:
            if link not in url_to_id:
                url_to_id[link] = unique_id_counter
                unique_id_counter += 1
            if url not in adjacency_list:
                adjacency_list[url] = []
            adjacency_list[url].append(link)
            if link not in incoming_edges_count:
                incoming_edges_count[link] = 0
            incoming_edges_count[link] += 1

    G = nx.Graph()
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    partition = community_louvain.best_partition(G)
    pagerank_scores = nx.pagerank(G, alpha=0.85)
    #hubs, authorities = nx.hits(G, max_iter=100, tol=1.0e-8)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-4)

    sorted_urls = sorted(pagerank_scores, key=pagerank_scores.get, reverse=True)
    #sorted_hubs = sorted(hubs, key=hubs.get, reverse=True)
    #sorted_authorities = sorted(authorities, key=authorities.get, reverse=True)
    sorted_betweenness_centrality = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)
    sorted_closeness_centrality = sorted(closeness_centrality, key=closeness_centrality.get, reverse=True)
    sorted_eigen_centralities = sorted(eigenvector_centrality, key=eigenvector_centrality.get, reverse=True)
    url_rank = {url: rank + 1 for rank, url in enumerate(sorted_urls)}
    #hubs_rank = {url: rank + 1 for rank, url in enumerate(sorted_hubs)}
    #authorities_rank = {url: rank + 1 for rank, url in enumerate(sorted_authorities)}
    betweenness_centralities_rank = {url: rank + 1 for rank, url in enumerate(sorted_betweenness_centrality)}
    closeness_centralities_rank = {url: rank + 1 for rank, url in enumerate(sorted_closeness_centrality)}
    eigen_centralities_rank = {url: rank + 1 for rank, url in enumerate(sorted_eigen_centralities)}

    written_ids = set()
    with open("output/constants.js", "w") as f:
        f.write('export const NODES = [')
        for url in url_to_id:
            size = incoming_edges_count.get(url, 0) + 1
            if url_to_id[url] not in written_ids:
                name = convert_wikipedia_url_to_text(url)
                num_edges = incoming_edges_count.get(url, 0)
                if name in PRESIDENTS:
                    f.write(f"{{id: {url_to_id[url]}, name: `{name}`, url: `{url}`, rank:{url_rank[url]}, page_rank:{pagerank_scores[url]}, betweenness_centrality: {betweenness_centrality[url]}, betweenness_centrality_rank:{betweenness_centralities_rank[url]}, closeness_centrality:{closeness_centrality[url]}, closeness_centrality_rank:{closeness_centralities_rank[url]}, eigen_centrality:{eigenvector_centrality[url]}, eigen_centrality_rank:{eigen_centralities_rank[url]}, num_edges:{num_edges}, partition: {partition[url]}, size: {size}, is_president: true}},\n")
                else:
                     f.write(f"{{id: {url_to_id[url]}, name: `{convert_wikipedia_url_to_text(url)}`, url: `{url}`, rank:{url_rank[url]}, page_rank:{pagerank_scores[url]}, betweenness_centrality: {betweenness_centrality[url]}, betweenness_centrality_rank:{betweenness_centralities_rank[url]}, closeness_centrality:{closeness_centrality[url]}, closeness_centrality_rank:{closeness_centralities_rank[url]}, eigen_centrality:{eigenvector_centrality[url]}, eigen_centrality_rank:{eigen_centralities_rank[url]}, num_edges:{num_edges}, partition: {partition[url]}, size: {size}}},\n")
                written_ids.add(url_to_id[url])
        f.write('];')

    with open("output/constants.js", "a") as f:
        f.write('export const EDGES = [')
        for url, links in adjacency_list.items():
            for link in links:
                f.write(f"{{source: {url_to_id[url]}, target: {url_to_id[link]}}},\n")
        f.write('];')

    with open("output/nodes_page_rank.txt", "w") as f:
        for url in sorted_urls:
            f.write(f"{convert_wikipedia_url_to_text(url)}: {pagerank_scores[url]}\n")

    # with open("output/nodes_hubs_rank.txt", "w") as f:
    #     for url in sorted_hubs:
    #         f.write(f"{convert_wikipedia_url_to_text(url)}: {hubs[url]}\n")

    # with open("output/nodes_authorities_rank.txt", "w") as f:
    #     for url in sorted_authorities:
    #         f.write(f"{convert_wikipedia_url_to_text(url)}: {authorities[url]}\n")

    with open("output/nodes_betweenness_centrality_rank.txt", "w") as f:
        for url in sorted_betweenness_centrality:
            f.write(f"{convert_wikipedia_url_to_text(url)}: {betweenness_centrality[url]}\n")

    with open("output/nodes_closeness_centrality_rank.txt", "w") as f:
        for url in sorted_closeness_centrality:
            f.write(f"{convert_wikipedia_url_to_text(url)}: {closeness_centrality[url]}\n")

    with open("output/nodes_eigen_centrality_rank.txt", "w") as f:
        for url in sorted_eigen_centralities:
            f.write(f"{convert_wikipedia_url_to_text(url)}: {eigenvector_centrality[url]}\n")


    print("Adjacency list, nodes, and links created and written to files")

def read_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def write_adjacency_list_to_file(adjacency_list, file_path):
    with open(file_path, 'w') as f:
        for url, links in adjacency_list.items():
            f.write(f"{url}:\n")
            for link in links:
                f.write(f"  {link}\n")

def run_web_scraper(input_file, output_file):
    urls = read_urls_from_file(input_file)
    url_set = set(urls)
    adjacency_list = {url: [] for url in urls}

    for url in urls:
        links = get_embedded_links(url)
        print('Processing:', url)
        for link in links:
            if link in url_set:
                adjacency_list[url].append(link)

    write_adjacency_list_to_file(adjacency_list, output_file)

run_presidential_election_web_scrapper()