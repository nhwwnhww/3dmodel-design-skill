import copy, hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from release_check import validate, input_digest
from assembly_check import screen
from checks_template import evaluate
class Gates(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.root.joinpath("build.py").write_text("source")
        self.root.joinpath("proof.txt").write_text("synthetic test evidence, not a real print")
        sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
        self.m={"schema_version":1,"revision":"r1","profile":{"printer":"P1S","nozzle_mm":0.4,"material":"PETG test","plate":"test","layer_height_mm":0.2},"inputs":{"build.py":sha("source")},"behavioral_claims":[],"assembly_required":False,"gates":{}}
        details={"build":{"command":"python build.py","tool_versions":"fixture"},"visual":{"views":["front","back","left","right","top","bottom","iso"],"sections":["X center","Z critical"],"findings":"fixture"},"dfam":{"orientation":"fixture","supports":"fixture","walls":"fixture","material_basis":"fixture"},"slice":{"slicer":"Bambu Studio","version":"fixture","profile":"fixture","warnings":"fixture","layer_review":"fixture"},"prototype":{"printer":"fixture","material":"fixture","observations":"fixture","feedback":"fixture"},"release":{"license":"fixture","originality":"fixture","limitations":"fixture"},"assembly":{"fit_table":"fixture","motion_path":"fixture"}}
        roles={"build":["build_log","model"],"visual":["views","sections"],"dfam":["report"],"slice":["project_3mf","preview"],"prototype":["report","photo"],"release":["listing","instructions"],"assembly":["report"]}
        for k,v in details.items():
            self.m["gates"][k]={"status":"passed","reviewer":"test fixture","revision":"r1","input_digest":input_digest(self.m),"details":v,"artifacts":[{"path":"proof.txt","sha256":sha("synthetic test evidence, not a real print"),"role":role} for role in roles[k]]}
    def test_complete_records(self): self.assertEqual(validate(self.m,self.root),[])
    def test_missing_gate(self):
        del self.m["gates"]["slice"];self.assertTrue(validate(self.m,self.root))
    def test_modified_source(self):
        self.root.joinpath("build.py").write_text("changed");self.assertTrue(validate(self.m,self.root))
    def test_modified_profile(self):
        self.m["profile"]["material"]="PLA";self.assertTrue(validate(self.m,self.root))
    def test_stale_revision(self):
        self.m["revision"]="r2";self.assertTrue(validate(self.m,self.root))
    def test_unknown_prototype(self):
        self.m["gates"]["prototype"]["status"]="unknown";self.assertTrue(validate(self.m,self.root))
    def test_no_sections(self):
        self.m["gates"]["visual"]["details"]["sections"]=[];self.assertTrue(validate(self.m,self.root))
    def test_missing_view(self):
        self.m["gates"]["visual"]["details"]["views"]=["iso"];self.assertTrue(validate(self.m,self.root))
    def test_fit_requires_assembly(self):
        self.m["behavioral_claims"]=["snap"];del self.m["gates"]["assembly"];self.assertTrue(validate(self.m,self.root))
    def test_bad_artifact_hash(self):
        self.m["gates"]["build"]["artifacts"][0]["sha256"]="0"*64;self.assertTrue(validate(self.m,self.root))
    def test_traversal(self):
        self.m["gates"]["build"]["artifacts"][0]["path"]="../outside";self.assertTrue(validate(self.m,self.root))
    def test_no_reviewer(self):
        self.m["gates"]["visual"]["reviewer"]="";self.assertTrue(validate(self.m,self.root))
    def test_wrong_slicer(self):
        self.m["gates"]["slice"]["details"]["slicer"]="Other";self.assertTrue(validate(self.m,self.root))
    def test_invalid_schema(self): self.assertTrue(validate({},self.root))
    def test_aabb_disjoint(self): self.assertEqual(screen([[0,0,0],[1,1,1]],[[2,0,0],[3,1,1]])["screen"],"disjoint")
    def test_aabb_overlap_not_collision_proof(self): self.assertEqual(screen([[0,0,0],[2,2,2]],[[1,1,1],[3,3,3]])["screen"],"possible_overlap")
    def test_aabb_contact(self): self.assertEqual(screen([[0,0,0],[1,1,1]],[[1,0,0],[2,1,1]])["screen"],"possible_contact")
    def test_bad_bounds(self):
        with self.assertRaises(ValueError): screen([[2,0,0],[1,1,1]],[[1,1,1],[2,2,2]])
    def test_behavior_needs_physical_details(self):
        self.m["behavioral_claims"]=["snap"]
        for gate in self.m["gates"].values(): gate["input_digest"]=input_digest(self.m)
        self.assertIn("prototype: missing physical behavior test snap",validate(self.m,self.root))
        self.m["gates"]["prototype"]["details"]["behavior_tests"]={"snap":"synthetic fixture report"}
        self.assertEqual(validate(self.m,self.root),[])
    def test_missing_role(self):
        self.m["gates"]["slice"]["artifacts"]=[];self.assertTrue(validate(self.m,self.root))
    def test_slice_only_scope(self):
        self.m["gates"]={"slice":self.m["gates"]["slice"]}
        self.assertEqual(validate(self.m,self.root,only=["slice"]),[])
        self.assertTrue(validate(self.m,self.root))
    def test_empty_numeric_checks(self):
        with self.assertRaises(ValueError): evaluate({"checks":[]})
    def test_numeric_range(self):
        data={"checks":[{"name":"width","unit":"mm","method":"fixture","source_revision":"r1","actual":5,"min":4,"max":6}]}
        self.assertTrue(evaluate(data)[0]["passed"])
        data["checks"][0]["actual"]=7;self.assertFalse(evaluate(data)[0]["passed"])
    def test_numeric_nan(self):
        with self.assertRaises(ValueError): evaluate({"checks":[{"name":"x","unit":"mm","method":"fixture","source_revision":"r1","actual":float('nan'),"min":0,"max":1}]})
    def test_numeric_reversed_limits(self):
        with self.assertRaises(ValueError): evaluate({"checks":[{"name":"x","unit":"mm","method":"fixture","source_revision":"r1","actual":1,"min":2,"max":0}]})
    def test_aabb_nan(self):
        with self.assertRaises(ValueError): screen([[0,0,0],[float('nan'),1,1]],[[1,1,1],[2,2,2]])
if __name__=="__main__": unittest.main()
