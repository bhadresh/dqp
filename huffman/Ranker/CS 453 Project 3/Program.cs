using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.XPath;
using System.IO;

namespace CS_453_Project_3
{
    class Program
    {
        static void Main(string[] args)
        {
            string filename = "sites.xml"; // Path to site xml map
 
            string Sites = "//Site"; // Get all site nodes
            string ID = "@ID";       // Get ID element
            string linksIn = "LinksFrom/ID";
            string linksOut = "LinksTo/ID";
            

            // Load site XML file
            XmlDocument document = new XmlDocument();
            
            try
            {
                document.Load(filename);
            }
            catch (IOException exc)
            {
                Console.WriteLine(exc.Message);
                Environment.Exit(1);
            } 


            XmlNodeList siteNodes = document.SelectNodes(Sites);
            double startPageRank = 1.0 / siteNodes.Count;

            double lamda = 0.15;

            /* Book -> aproaches 1 as lamda aproaches 1 */
            double PR = lamda / siteNodes.Count;    
            double Q = 1 - lamda;

            /* Wikipedia -> aproaches 1 as lamda aproaches 0 */
            //double PR = (1.0 - lamda) / siteNodes.Count;
            //double Q = lamda;

            /* Wikipedia -> aproaches N as lamda aproaches 0 */
            //double PR = (1.0 - lamda);
            //double Q = lamda;


            //Console.WriteLine(startPageRank);
            //Console.WriteLine(PR);
            //Console.WriteLine(Q);

            Dictionary<int, DocData> siteData = new Dictionary<int, DocData>();
            List<int> sitesToRank = new List<int>();

            XmlNode idAttribute;
            XmlNodeList idNodes;           
            foreach(XmlNode siteNode in siteNodes)
            {

                DocData D = new DocData();
                idAttribute = siteNode.SelectSingleNode(ID); // Gets the DocID node

                // Get all the links in
                idNodes = siteNode.SelectNodes(linksIn);
                foreach (XmlNode idNode in idNodes)
                {
                    D.LinksIn.Add(int.Parse(idNode.InnerText));
                }

                sitesToRank.Add(int.Parse(idAttribute.Value));

                // Get all the links out .. we only really care about the amount
                idNodes = siteNode.SelectNodes(linksOut);

                D.LinksOutCount = idNodes.Count;
                D.PageRank = startPageRank; // Sets the initial page rank

                // Add the site and its data
                siteData.Add(int.Parse(idAttribute.Value), D);              
            }

            // Page rank algorithm
            double MaxChange = 1;
            while (MaxChange > 0.000000000001)
            {
                //Console.WriteLine(MaxChange);
                MaxChange = 0;
                
                foreach (int id in sitesToRank)
                {
                    double newPageRank = 0.0;

                    // Add all the ranks of pages linking to the site
                    foreach (int pageid in siteData[id].LinksIn)
                    {
                        newPageRank += (siteData[pageid].PageRank / siteData[pageid].LinksOutCount);
                    }

                    newPageRank = newPageRank * Q + PR; // Calculate new page rank

                    double difference = Math.Abs(newPageRank - siteData[id].PageRank);
                    if (difference > MaxChange)
                    {
                        MaxChange = difference;
                    }
                    
                    siteData[id].PageRank = newPageRank; //set the new rank to this document
                } 
            }

            double total = 0;

            // Write out to file
            try 
            {
                using(StreamWriter fstr_out = new StreamWriter("out.txt"))
                {
                    foreach(KeyValuePair<int, DocData> kvp in siteData)
                    {
                        fstr_out.Write(kvp.Key.ToString() 
                            + ":" 
                            + String.Format("{0:0.000000000000000}", kvp.Value.PageRank) 
                            + Environment.NewLine);

                        total += kvp.Value.PageRank;
                    }
                }
            }
            catch (IOException exc)
            {
                Console.WriteLine(exc.Message);
                Environment.Exit(2);
            }
            //Console.WriteLine(total);
            //Console.ReadLine();
        }
    }
}
