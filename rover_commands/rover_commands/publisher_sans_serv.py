import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import curses

class TrajectoryPublisher(Node):

    def __init__(self, stdscr):
        super().__init__('trajectory_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Publisher node has been started.')
        
        # Configuration de curses pour le mode non-bloquant
        self.stdscr = stdscr
        self.stdscr.nodelay(True)  # Ne pas bloquer en attente d'une touche
        self.stdscr.clear()

        # Timer pour vérifier les entrées de touches
        self.timer = self.create_timer(0.1, self.cmd_acquisition)

    def cmd_acquisition(self):
        msg = Twist()  # Créer un message Twist vide

        # Lire la touche pressée
        key = self.stdscr.getch()

        # Assigner les valeurs en fonction de la touche pressée
        if key == ord('w'):  # Avancer
            msg.linear.x = 1.0
        elif key == ord('s'):  # Reculer
            msg.linear.x = -1.0
        elif key == ord('a'):  # Tourner à gauche
            msg.angular.z = 1.0
        elif key == ord('d'):  # Tourner à droite
            msg.angular.z = -1.0
        elif key == ord('t'):  # Arrêt
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        # Publier le message seulement si une touche pertinente est pressée
        if msg.linear.x != 0.0 or msg.angular.z != 0.0:
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)  # Initialiser ROS 2 pour Python
    # Initialiser curses pour capturer les entrées sans "Entrée"
    curses.wrapper(lambda stdscr: rclpy.spin(TrajectoryPublisher(stdscr)))
    rclpy.shutdown()

if __name__ == '__main__':
    main()
