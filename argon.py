#!/usr/bin/env python3
"""Gemini 4 Argon 호출 데모 (Gemini API, 스트리밍). 키는 환경변수 GEMINI_API_KEY.
사용: argon.py --info | argon.py "프롬프트" [--out 파일] [--quiet]"""
import json, os, sys, time, urllib.request

MODEL = "gemini-4-argon"
BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
KEY = os.environ["GEMINI_API_KEY"]
B, D, C, Y, G, R = "\033[1m", "\033[2m", "\033[36m", "\033[33m", "\033[32m", "\033[0m"


def req(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                               headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    return urllib.request.urlopen(r, timeout=600)


def info():
    m = json.load(req(BASE + MODEL))
    print(f"{B}{m['displayName']}{R}  {D}({m['name']}){R}")
    print(f"  입력 한도   {Y}{m['inputTokenLimit']:,}{R} 토큰")
    print(f"  출력 한도   {Y}{m['outputTokenLimit']:,}{R} 토큰")
    print(f"  생각 모드   {G}{'켜짐' if m.get('thinking') else '없음'}{R}")


def run(prompt, out=None, quiet=False):
    print(f"{C}▶ {MODEL}{R} {D}스트리밍 호출{R}\n")
    t0 = time.time(); first = None; text = []; usage = {}
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    with req(BASE + MODEL + ":streamGenerateContent?alt=sse", body) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data:"):
                continue
            d = json.loads(line[5:])
            usage = d.get("usageMetadata", usage)
            for c in d.get("candidates", []):
                for p in c.get("content", {}).get("parts", []):
                    if p.get("text") and not p.get("thought"):
                        first = first or time.time()
                        text.append(p["text"])
                        if not quiet:
                            print(p["text"], end="", flush=True)
    full = "".join(text)
    if out:
        if out.endswith(".html") and "```" in full:
            full = full.split("```", 1)[1].split("\n", 1)[1].rsplit("```", 1)[0]
        open(out, "w").write(full)
    dt = time.time() - t0
    print(f"\n\n{D}──────────────{R}")
    if out:
        print(f"저장  {G}{out}{R}  ({len(full):,}자)")
    print(f"첫 글자 {Y}{(first or time.time()) - t0:.1f}초{R} · 전체 {Y}{dt:.1f}초{R}")
    print(f"토큰  입력 {usage.get('promptTokenCount', 0):,} · 출력 {usage.get('candidatesTokenCount', 0):,}"
          f" · 생각 {usage.get('thoughtsTokenCount', 0):,}")
    json.dump({"prompt": prompt, "seconds": round(dt, 2), "first_token_s": round((first or t0) - t0, 2),
               "usage": usage, "chars": len(full)}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_run.json"), "w"), ensure_ascii=False)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--info":
        info()
    else:
        out = a[a.index("--out") + 1] if "--out" in a else None
        run(a[0], out, "--quiet" in a)
