#!/usr/bin/env python3
import requests
from datetime import datetime

def get_trending_repos():
    from datetime import timedelta
    url = "https://api.github.com/search/repositories"
    seven_days_ago = datetime.now() - timedelta(days=7)
    params = {
        "q": "created:>" + seven_days_ago.strftime("%Y-%m-%d"),
        "sort": "stars",
        "order": "desc",
        "per_page": 20
    }
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def format_repos(repos):
    lines = []
    lines.append(f"# GitHub Trending Repositories - {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append("Updated daily at UTC 00:00\n")
    lines.append("| Rank | Repository | Stars | Description | Language |")
    lines.append("|------|------------|-------|-------------|----------|")
    
    for i, repo in enumerate(repos["items"], 1):
        description = repo['description'] if repo['description'] else "No description"
        truncated_desc = description[:100] + "..." if len(description) > 100 else description
        lines.append(
            f"| {i} | [{repo['full_name']}]({repo['html_url']}) | ⭐ {repo['stargazers_count']:,} | {truncated_desc} | {repo.get('language', 'Unknown')} |"
        )
    
    return "\n".join(lines)

def main():
    try:
        repos = get_trending_repos()
        if not repos or "items" not in repos:
            print("Error: No repositories found in API response")
            return 1
        
        content = format_repos(repos)
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Successfully updated README.md with {len(repos['items'])} trending repos")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0

if __name__ == "__main__":
    exit(main())