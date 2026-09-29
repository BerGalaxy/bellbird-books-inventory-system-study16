from flask import request

# Feat: MSD426GXUST16-5 add search and filter logic
@app.route('/search')
def search_books():
    query = request.args.get('q', '')
    if not query:
        return {"message": "Please provide a search query"}
    
    # 模拟搜索逻辑（后续由后端队友连接数据库）
    matched_books = []
    
    return {"message": f"Searching for: {query}", "results": matched_books}