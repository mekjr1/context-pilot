from contextpilot.context.freshness import check_source
def test_f(tmp_path):
 p=tmp_path/"x.txt"; p.write_text("a"); assert check_source(str(p))["type"]=="local_file"
