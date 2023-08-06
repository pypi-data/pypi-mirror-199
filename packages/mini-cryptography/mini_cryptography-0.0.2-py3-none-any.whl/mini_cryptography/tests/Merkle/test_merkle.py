from mini_cryptography.merkle import Merkle
from parameterized import parameterized
from unittest.mock import patch

@parameterized.expand([
    (Merkle.SHA.SHA1, '67bde3f17201172d8aff4cd976870cecb24a626d'),
    (Merkle.SHA.SHA224, '6cae89a9b682db1d788b247c65a4be1f56cf995bb0cb5c5b7cba0606'),
    (Merkle.SHA.SHA256, '92599579e207c2553a712247ab0f2026876d2b078324b724e709d715d22e6dbb'),
    (Merkle.SHA.SHA3_224, 'a1972671038e3d973cb2c1c10975b79d084ac57b8a1b924ef527a4bb'),
    (Merkle.SHA.SHA3_256, 'a4c87dd2f3405bae2ab3cbfca20d841fdd669c81888132275ffe62af3030854b'),
    (Merkle.SHA.SHA3_384, '63cea80ac5ec42cee4940665bd43f444254bdb22b4271b85d6489ab9ac528311004a9d0bee532eadea20546696a63049'),
    (Merkle.SHA.SHA3_512, '1470a1fad2e37ed8f26c15314437cba1cdd72ef2b58860c46c58f0e05f6aa7e7f9ab2097fea75500254c30c9a989231eb8a843844c0f128d2022e6ac5f2c36f4'),
    (Merkle.SHA.SHA512, '310fd3f17291c07f792dedeb2f06ccfd4e0c56157ebc6e7fad105586dae71af2d83db50f10bdd9626e85a89446fe5c209cf7733f5ff3cb073902d8676693f2a4'),
    (Merkle.SHA.SHAKE_128, '9e9a9a35d3abab4e4d791c78a3e061c27da2ac124e7fba68a913821e2a1dd8f81014819da8ebc86a60493de5124cffdf37a90c2a9d22da0346050c9df4a587690508bc78958143783dcd7ffd6ab66cc99ceb65298bf700ea9fb444ce209a2e6f881d968e'),
    (Merkle.SHA.SHAKE_256, 'ec67714c508a3b68688a15f625cef1f60344aba9ba19c51242c11ca816fdce048bc2f9a354092b3fb9ae0f75314a5d0526867496a7bd2cd869ba6e93e51bdf4edb47c578ded852eb4a64cecce66a33fa34c67827c3c3f82736bd2616aa3a57963a83f4f5')
])
def test_merkle_root_hashed(sha:Merkle.SHA, expected:str):
    hashList = [
        '01000000295c297aee86096dcf6092',
        '0100000007bdc63ab3e74058a87b92',
        '01000000017b23260463311a4d1936',
        '0100000007bdc63ab3e74058a87b92'
    ]
    
    assert Merkle(sha).merkle_root(hashList, 0) == expected

@parameterized.expand([
    (Merkle.SHA.SHA1, 'a0211de60fb068ed36a619c122e79cc76610f906'),
    (Merkle.SHA.SHA224, 'e8c4455fc750c8ae8acba8ddee4c7007b88e29a4d3df606743dec913'),
    (Merkle.SHA.SHA256, 'dab723ee8eb19d22d652b55cb0915c04b00d745796dda8df0590696c91d0b4b2'),
    (Merkle.SHA.SHA3_224, '407dd003f5ccfbc0053555b5efd75508bd027878058a94afa7f28e4b'),
    (Merkle.SHA.SHA3_256, 'cd10ca15e56ee5b7ceb821e3149d59e0434bd68dc0f74adbefd09e6b39ae5428'),
    (Merkle.SHA.SHA3_384, '823a2c674770986dd36914c63de4913fd2d512af9229682af6b553fcfbfcf65b22466459e522732d8abbdae435a60256'),
    (Merkle.SHA.SHA3_512, 'e315da6fea472b5fe74c48f4d1fd7f0e1eb11bef0508fdf200e512147be1e3d459a862c904ca075480497bfeea9c3bcbad6de3e5311f89d547b22c5f55062c90'),
    (Merkle.SHA.SHA512, '169a1c96ca1bf724ab8cfc567cfd7406b61700d3bac20003d8e058888e670b9c2700bbbbe58d2f4a45bee08922965146102a32277cc1d71303ef58f829575bb4'),
    (Merkle.SHA.SHAKE_128, 'e59ae3ace33a8e4880252e2225922ddac93b01d4c355956c3a25268fc31b9a23505b3dbf20b6027bef6da437bc798b11c222140e16668127fcb9b75530dbdf7af2ae04090dafba9397cc56f674de7327622ba6d98ed78321e260a2a2eaca104f9b023692'),
    (Merkle.SHA.SHAKE_256, '3f3b06f6b303ea8b6003333e61be80caab9fe19ceefc59428ccb0ed0cb64c842b997c6c6995aaa7a27e77375d4394fecb18337cf9b15eb36dd3ee3ebc530d9be84d152c3c2c78e9123f8d3ea8447ad0035ecab0abb585c3d4bfa5db3c266cea02bb1b11e')
])
def test_merkle_root_not_hashed(sha:Merkle.SHA, expected:str):
    hashList = [
        '01000000295c297aee86096dcf6092',
        '0100000007bdc63ab3e74058a87b92',
        '01000000017b23260463311a4d1936',
        '0100000007bdc63ab3e74058a87b92'
    ]

    assert Merkle(sha).merkle_root(hashList, 1) == expected  

def test_merkle_root_number_of_hashed_pairs_is_odd():
    hashList = [
        '01000000295c297aee86096dcf6092',
        '0100000007bdc63ab3e74058a87b92',
        '01000000017b23260463311a4d1936',
    ]

    assert Merkle(Merkle.SHA.SHA256).merkle_root(hashList, 0) == 'bb87c6b0fb70555455793c27c142817710ac23e166ae4f2a2165e4795ea7e53e'

@patch('mini_cryptography.merkle')
def test_merkle_root_not_existing_hash(mock):
    hashList = [
        '01000000295c297aee86096dcf6092',
        '0100000007bdc63ab3e74058a87b92',
        '01000000017b23260463311a4d1936',
        '0100000007bdc63ab3e74058a87b92'
    ]
    mock.SHA.SHA16 = -1

    assert Merkle(mock.SHA.SHA16).merkle_root(hashList, 0) == '92599579e207c2553a712247ab0f2026876d2b078324b724e709d715d22e6dbb'

@parameterized.expand([
    (Merkle.SHA.SHA1, '5ef998d9c1649f599c7241257c2f52725a9e1703'),
    (Merkle.SHA.SHA224, '8a48ba623fba96228467d445894c1900e3ebdd9e050a1332975db80c'),
    (Merkle.SHA.SHA256, 'cb8c31af6e9fff0daab6fd09cb548dc44d1178bb3f35c175b4bf22a0e48d93ea'),
    (Merkle.SHA.SHA3_224, 'df2631ba5d74fce401acc5232ef3a864d9919087f41589480bd2f1d0'),
    (Merkle.SHA.SHA3_256, '45bde44882c2aa87fedbe2d290684c8032e018aea449087d1332800907a99c72'),
    (Merkle.SHA.SHA3_384, 'b4a5cb19f0700cec4bf8775f3c062935b44e2d05eb96c4f5830f9f2ad5f36f1021f7dc8f3f628f34e663b243c9c9a8de'),
    (Merkle.SHA.SHA3_512, 'c2364ab22b01fdd5a2f20d5a1f9a386696c2151b2f00617007fdddb8bda1b7fa93a57a06b8174f44d4079a6b93e25d112982d66ef205c951dea56a5061f51f33'),
    (Merkle.SHA.SHA512, '41b7d651b29c48c5d941d4e9474d289958ff95e621fa34fe7277707cea2d6166ec13611d3485438921bd313fa9e9b555226a42cb7d99f7d67711a1b2b097d4a0'),
    (Merkle.SHA.SHAKE_128, 'b5e881af6391c00b68247d77a8ed12ac4fa6c861f5b87cca70126704c3ae259fac410e7d380f32717160cc4d2bb888edcc97f96816b16a19076c5f3aa42d5c3ba9039c2033119e6d9ee8309015c4cae5104665952004e8b7ae40a1a2f88026921e7efa39'),
    (Merkle.SHA.SHAKE_256, 'ee5c2c6a3a970b2289644231b530301074d8c5b9930527d087eed0f4640e16875aae48408ae338c9869253d8e92b017d4e3095431063e92bb32d8210e6655242b9f5b60924a8c30c7ff501cad581cdb313e44e2caf0039fde82932cb05bd28ff00ed9ceb')
])
def test_calculate_hash(sha:Merkle.SHA, expected:str):
    hash = '01000000295c297aee86096dcf6092'.encode('utf8')

    assert Merkle(sha).calculate_hash(hash).hex() == expected

def test_shift_hash():
    hash = '01000000295c297aee86096dcf6092'
    assert Merkle().shift_hash(hash) == b'9260cf6d0986ee7a295c2900000001'

def transaction_hash():
    hash = '01000000295c297aee86096dcf6092'
    expected = b'3860b826dfc02feed1bbeb908eb0b2c0f5ea32a1b12ef1e8d87d2bf0e3802795'
    assert Merkle().transaction_hash(hash) == expected