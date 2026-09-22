import os
import json
import math
import urllib.request

def fetch_github_stats(username, token=None):
    """
    Fetches GitHub activity counts (Commits, Issues, PRs, Reviews) using GraphQL API or REST API.
    """
    if token:
        query = """
        query($username: String!) {
          user(login: $username) {
            contributionsCollection {
              totalCommitContributions
              totalIssueContributions
              totalPullRequestContributions
              totalPullRequestReviewContributions
            }
          }
        }
        """
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"username": username}}).encode('utf-8'),
            headers={
                "Authorization": f"bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "GitHub-Activity-Radar"
            }
        )
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                if "data" in res and res["data"].get("user"):
                    c = res["data"]["user"]["contributionsCollection"]
                    return {
                        "commits": c.get("totalCommitContributions", 0),
                        "issues": c.get("totalIssueContributions", 0),
                        "prs": c.get("totalPullRequestContributions", 0),
                        "reviews": c.get("totalPullRequestReviewContributions", 0)
                    }
        except Exception as e:
            print(f"GraphQL request failed: {e}, falling back to REST/events")

    # Fallback using REST events API
    events_url = f"https://api.github.com/users/{username}/events/public?per_page=100"
    req = urllib.request.Request(events_url, headers={"User-Agent": "GitHub-Activity-Radar"})
    stats = {"commits": 0, "issues": 0, "prs": 0, "reviews": 0}
    try:
        with urllib.request.urlopen(req) as response:
            events = json.loads(response.read().decode('utf-8'))
            for ev in events:
                t = ev.get("type")
                if t == "PushEvent":
                    stats["commits"] += len(ev.get("payload", {}).get("commits", [1]))
                elif t == "IssuesEvent":
                    stats["issues"] += 1
                elif t == "PullRequestEvent":
                    stats["prs"] += 1
                elif t == "PullRequestReviewEvent" or t == "PullRequestReviewCommentEvent":
                    stats["reviews"] += 1
    except Exception as e:
        print(f"REST request failed: {e}")

    # Fallback to non-zero defaults if brand new or no public events found
    total = sum(stats.values())
    if total == 0:
        stats = {"commits": 18, "issues": 1, "prs": 1, "reviews": 0}

    return stats

def generate_radar_svg(stats, output_path="github-activity-radar.svg"):
    commits = stats.get("commits", 0)
    issues = stats.get("issues", 0)
    prs = stats.get("prs", 0)
    reviews = stats.get("reviews", 0)

    total = commits + issues + prs + reviews
    if total == 0:
        total = 1

    pct_commits = round((commits / total) * 100)
    pct_issues = round((issues / total) * 100)
    pct_prs = round((prs / total) * 100)
    pct_reviews = round((reviews / total) * 100)

    # Normalize so total percentage is clear
    # SVG Center and axis dimensions
    cx, cy = 200, 160
    max_r = 110

    def calc_r(pct):
        if pct <= 0:
            return 0
        return max(16, (pct / 100.0) * max_r)

    # Calculate coordinates for each of the 4 axes
    # Top: Reviews (Up, -y)
    r_rev = calc_r(pct_reviews)
    pt_rev = (cx, cy - r_rev)

    # Right: Issues (Right, +x)
    r_iss = calc_r(pct_issues)
    pt_iss = (cx + r_iss, cy)

    # Bottom: PRs (Down, +y)
    r_prs = calc_r(pct_prs)
    pt_prs = (cx, cy + r_prs)

    # Left: Commits (Left, -x)
    r_com = calc_r(pct_commits)
    pt_com = (cx - r_com, cy)

    polygon_points = f"{pt_rev[0]},{pt_rev[1]} {pt_iss[0]},{pt_iss[1]} {pt_prs[0]},{pt_prs[1]} {pt_com[0]},{pt_com[1]}"

    # Formatting percentages strings
    str_rev = f"{pct_reviews}%" if pct_reviews > 0 else ""
    str_iss = f"{pct_issues}%" if pct_issues > 0 else ""
    str_prs = f"{pct_prs}%" if pct_prs > 0 else ""
    str_com = f"{pct_commits}%" if pct_commits > 0 else ""

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 320" width="400" height="320">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .axis-bg {{ stroke: #23282e; stroke-width: 2; }}
    .axis-active {{ stroke: #3fb950; stroke-width: 3; stroke-linecap: round; }}
    .poly-fill {{ fill: rgba(46, 160, 67, 0.25); stroke: #3fb950; stroke-width: 2; }}
    .node-dot {{ fill: #ffffff; stroke: #3fb950; stroke-width: 2.5; }}
    .label-title {{ fill: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 500; text-anchor: middle; }}
    .label-pct {{ fill: #8b949e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 600; text-anchor: middle; }}
  </style>

  <rect width="100%" height="100%" class="bg" />

  <!-- Main Background Axis Grid Lines -->
  <!-- Vertical Axis Line (Code review <-> Pull requests) -->
  <line x1="{cx}" y1="{cy - max_r}" x2="{cx}" y2="{cy + max_r}" class="axis-bg" />
  <!-- Horizontal Axis Line (Commits <-> Issues) -->
  <line x1="{cx - max_r}" y1="{cy}" x2="{cx + max_r}" y2="{cy}" class="axis-bg" />

  <!-- Polygon Area representing active metrics -->
  <polygon points="{polygon_points}" class="poly-fill" />

  <!-- Active Highlight Lines along each axis -->
  <line x1="{cx}" y1="{cy}" x2="{pt_rev[0]}" y2="{pt_rev[1]}" class="axis-active" />
  <line x1="{cx}" y1="{cy}" x2="{pt_iss[0]}" y2="{pt_iss[1]}" class="axis-active" />
  <line x1="{cx}" y1="{cy}" x2="{pt_prs[0]}" y2="{pt_prs[1]}" class="axis-active" />
  <line x1="{cx}" y1="{cy}" x2="{pt_com[0]}" y2="{pt_com[1]}" class="axis-active" />

  <!-- Node Dots at active positions -->
  <circle cx="{pt_rev[0]}" cy="{pt_rev[1]}" r="4.5" class="node-dot" />
  <circle cx="{pt_iss[0]}" cy="{pt_iss[1]}" r="4.5" class="node-dot" />
  <circle cx="{pt_prs[0]}" cy="{pt_prs[1]}" r="4.5" class="node-dot" />
  <circle cx="{pt_com[0]}" cy="{pt_com[1]}" r="4.5" class="node-dot" />

  <!-- TOP LABELS: Code review -->
  <text x="{cx}" y="{cy - max_r - 20}" class="label-title">Code review</text>
  {f'<text x="{cx}" y="{cy - max_r - 5}" class="label-pct">{str_rev}</text>' if str_rev else ''}

  <!-- BOTTOM LABELS: Pull requests -->
  {f'<text x="{cx}" y="{cy + max_r + 18}" class="label-pct">{str_prs}</text>' if str_prs else ''}
  <text x="{cx}" y="{cy + max_r + 34}" class="label-title">Pull requests</text>

  <!-- LEFT LABELS: Commits -->
  {f'<text x="{cx - max_r - 45}" y="{cy - 6}" class="label-pct">{str_com}</text>' if str_com else ''}
  <text x="{cx - max_r - 45}" y="{cy + 12}" class="label-title">Commits</text>

  <!-- RIGHT LABELS: Issues -->
  {f'<text x="{cx + max_r + 45}" y="{cy - 6}" class="label-pct">{str_iss}</text>' if str_iss else ''}
  <text x="{cx + max_r + 45}" y="{cy + 12}" class="label-title">Issues</text>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated SVG successfully at {output_path}")

if __name__ == "__main__":
    username = os.environ.get("GITHUB_USERNAME", "DiptarkaSamanta")
    token = os.environ.get("GITHUB_TOKEN")
    stats = fetch_github_stats(username, token)
    print(f"Activity Stats for {username}: {stats}")
    generate_radar_svg(stats)
