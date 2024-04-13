public class InsertNode {
    // Linked list node structure
    class Node {
        int data;
        Node next;

        public Node(int data) {
            this.data = data;
            this.next = null;
        }
    }

    public Node head = null;
    public Node tail = null;

    // addNode() it will add a new node at the end of the linked list
    public void addNode(int data) {
        // Creating a new node
        System.out.println("Adding a new node with value "+data+" at the end of the linked list ");
        Node new_Node = new Node(data);

        // it will check if the list is empty or not
        if (head == null) {
            // when list is empty,head and tail point to new node
            head = new_Node;
            tail = new_Node;
        } else {
            // new_Node will be added after tail such that tail's next will point to newNode
            tail.next = new_Node;
            // new_Node will become new tail of the list
            tail = new_Node;
        }
    }

    // PrintData() will display all the nodes present in the list
    public void PrintData() {

        Node current = head;
        if (head == null) {
            System.out.println("Linked List is empty");
            return;
        }
        while (current != null) {
            // It will print each node by incrementing pointer
            System.out.print(current.data + " ");
            current = current.next;
        }
        System.out.println();
    }

    public static void main(String[] args) {

        InsertNode List = new InsertNode();

        // Add 5 to the end of the list
        List.addNode(5);
        List.PrintData();

        // Add 4 to the end of the list
        List.addNode(4);
        List.PrintData();

        // Add 3 to the end of the list
        List.addNode(3);
        List.PrintData();

        // Add 2 to the end of the list
        List.addNode(2);
        List.PrintData();
    }
}