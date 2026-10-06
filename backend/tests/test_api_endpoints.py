"""
API End-to-End Integration Test Suite
Verifies full user journeys: sample analysis, dashboard statistics aggregation,
history retrieval with filters, and deletion.
"""

def test_sample_analysis_and_dashboard_flow(client, auth_headers):
    # 1. Trigger sample analysis
    response = client.post("/api/analysis/sample", headers=auth_headers)
    assert response.status_code == 201
    analysis_data = response.json()
    assert analysis_data["job_title"] == "Junior Python Developer"
    assert analysis_data["match_score"] > 60.0
    assert len(analysis_data["matching_skills"]) > 0
    analysis_id = analysis_data["id"]

    # 2. Verify Dashboard stats updated
    dash_resp = client.get("/api/dashboard/stats", headers=auth_headers)
    assert dash_resp.status_code == 200
    stats = dash_resp.json()
    assert stats["total_analyses"] >= 1
    assert stats["average_score"] > 0
    assert len(stats["recent_analyses"]) >= 1

    # 3. Retrieve analysis history list
    list_resp = client.get("/api/analysis", headers=auth_headers)
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(item["id"] == analysis_id for item in items)

    # 4. Search analysis history
    search_resp = client.get("/api/analysis?search=Python", headers=auth_headers)
    assert search_resp.status_code == 200
    search_items = search_resp.json()
    assert len(search_items) >= 1

    # 5. Fetch single analysis detail
    detail_resp = client.get(f"/api/analysis/{analysis_id}", headers=auth_headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == analysis_id

    # 6. Delete analysis
    del_resp = client.delete(f"/api/analysis/{analysis_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    # 7. Confirm deletion
    get_del = client.get(f"/api/analysis/{analysis_id}", headers=auth_headers)
    assert get_del.status_code == 404
