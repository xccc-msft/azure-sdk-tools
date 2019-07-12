﻿using System.Collections.Generic;
using System.Threading.Tasks;
using APIViewWeb.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;

namespace APIViewWeb.Pages.Assemblies
{
    public class IndexModel : PageModel
    {
        private readonly BlobAssemblyRepository assemblyRepository;

        public IndexModel(BlobAssemblyRepository assemblyRepository)
        {
            this.assemblyRepository = assemblyRepository;
        }

        public List<(string id, string name)> Assemblies { get; set; }

        public async Task OnGetAsync()
        {
            Assemblies = await assemblyRepository.FetchAssembliesAsync();
        }
    }
}