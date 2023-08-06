import hashlib
import unittest
from mini_cryptography.ecdsa import Field, Point, Ecdsa
from parameterized import parameterized
from unittest.mock import patch

class TestClass(unittest.TestCase):

    def setup_class(self):
        # Data
        a = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112316
        b = 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575
        n = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
        p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
        G = Point(
            26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087,
            8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871
        )

        self.secp384r1 = Field(a, b, n, p, G)
        self.ecdsa = Ecdsa(self.secp384r1, name="secp384r1")

        self.point1 = Point(
            19577993669543055159462232654227477804059834554938749056365059575367343238573934152231932832497698572508881172084304,
            34797297628126597108728033628292920232095535295240081944254459873403593475466847089395925227525676205111687199013609
        )

        self.point2 = Point(
            2643888095364097454558349481745047911629089192351741699089972264282318601908091592262966275642198233545325090846186,
            12384549089646028340756024322986515983214437514151244063613237375835994573258040845173892755352541890195338888681840
        )

        self.privateKey = 20989443543778090555157442102131049817299902423795685309899862760056430951462397686708870733055917820122718887042439
        self.message = 'Religio, Doctrina, Civilitas, prae omnibus Virtus'
        self.hash = int(hashlib.sha1(self.message.encode()).hexdigest(),base=16)
        self.k = 11000
        self.r = 22152009089199730593582524338115427010336291169893373839910753311913746007332469659451755453856401184556487920772225 
        self.s = 33247802217962351080804096577524498301009516670239406026864057032340769378746165513387841747729702616554540985061660
        
        self.public_key = Point(
            30040694804942853208177610713088115928148181688856632998897580287365858436344609590182460206850552050293936278998346,
            17559245262757783022105893899857708160332511010412356224688036071313308531776780869864952047367968387454976435887533
        )
        # Results
        self.point = Point(
            30040694804942853208177610713088115928148181688856632998897580287365858436344609590182460206850552050293936278998346,
            17559245262757783022105893899857708160332511010412356224688036071313308531776780869864952047367968387454976435887533
        )

    def test_get_name(self):
        assert self.ecdsa.getName() == "secp384r1"

    def test_g_multiplication(self):
        assert self.ecdsa.G_multiplication(self.privateKey) == self.point

    def test_calculate_public_key(self):
        assert self.ecdsa.calculate_public_key(self.privateKey) == self.point

    def test_sum_points(self):
        point = Point(
            22152009089199730593582524338115427010336291169893373839910753311913746007332469659451755453856401184556487920772225,
            21415530147108271193135517297779083081913015961082356748098427685923206883047231450346172563957532258197936273940105
        )

        assert self.ecdsa.sum_points(self.point1, self.point2) == point

    def test_multiply_points(self):
        multiplier = 9868959070921577617284768940259093768032668379810297735137924030066340321810481073797782613683403119141615137083587
        point = Point(
            14103764458811902000156928461250459647654661504776098395816220167714718139473397796549037360732342313833270939242263,
            17395148190829553535748807655250157906889415207238492158034708401150356646081290450883354819984464883347616139045011
        )

        assert self.ecdsa.multiply_points(self.point1, multiplier) == point
    
    def test_generate_random_number(self):
        number = self.ecdsa.generate_random_number(1, self.secp384r1.n-1)
        assert number > 1 and number < self.secp384r1.n

    def test_k_generator(self):
        number = self.ecdsa.k_generator()
        assert number > 1 and number < self.secp384r1.n

    def test_private_key_generator(self):
        number = self.ecdsa.private_key_generator()
        assert number > 1 and number < self.secp384r1.n

    def test_sign_message(self):  
        assert self.ecdsa.sign_message(self.privateKey, self.k, self.hash) == (self.r, self.s)

    def test_sign_message_component_r_zero(self):
        with patch.object(Ecdsa, 'G_multiplication', return_value=Point(self.secp384r1.n, 0)):
            assert self.ecdsa.sign_message(0, 1, 0) == 0

    def test_sign_message_component_s_zero(self):  
        assert self.ecdsa.sign_message(0, 1, 0) == 1

    def test_verify_signature(self):
        verification = self.ecdsa.verify_signature(self.r, self.s, self.hash, self.public_key)
        assert verification

    @parameterized.expand([
        (2, 1),
        (1, 2),
        (-1, 1),
        (1, -1)
    ])
    def test_verify_signature_false_s_and_r_components(self, rm:int, sm:int):
        verification = self.ecdsa.verify_signature(self.r * rm, self.s * sm, self.hash, self.public_key)
        assert not verification

    def test_verify_signature_false_r(self):
        verification = self.ecdsa.verify_signature(self.r + 1, self.s, self.hash, self.public_key)
        assert not verification
