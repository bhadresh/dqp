using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CS_453_Project_3
{
    class DocData
    {
        public DocData(){
            linksIn = new List<int>();
        }
        private int linksOutCount;
        private double pageRank;
        private List<int> linksIn;


        public int LinksOutCount
        {
            get
            {
                return linksOutCount;
            }
            set
            {
                linksOutCount = value;
            }
        }

        public double PageRank
        {
            get
            {
                return pageRank;
            }
            set
            {
                pageRank = value;
            }
        }

        public List<int> LinksIn
        {
            get
            {
                return linksIn;
            }
        }
    }
}
