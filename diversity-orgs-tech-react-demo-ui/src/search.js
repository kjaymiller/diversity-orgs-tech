import React from "react";

import {
  buildAutocompleteQueryConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
} from "./config/config-helper";

import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector";
import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch, 
} from "@elastic/react-search-ui";


import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";


import Result from "./result";
import SortingView from './SortingView';
import _MultiCheckboxFacet from './FacetView';
import MultiCheckboxFacet from './inlineFacetView';

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new AppSearchAPIConnector({
  searchKey,
  engineName,
  hostIdentifier,
  endpointBase
});
const config = {
  searchQuery: {
    facets: {
        city: {
            type: "value",
            size: 30,
        },
        technology_focus: {
            type: "value",
            size: 30,
        },
        diversity_focus: {
            type: "value",
            size: 30,
        },
        parent_organization: {
            type: "value",
            size: 30,
        }
    },
    ...buildSearchOptionsFromConfig()
  },
  autocompleteQuery: buildAutocompleteQueryConfig(),
  apiConnector: connector,
  alwaysSearchOnInitialLoad: false
};


export default function Search() {

  return (
    <div className="container px-2 mx-auto my-4">
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                      <Facet
                        field="parent_organization"
                        label="Parent Organization"
                        view={_MultiCheckboxFacet}
                        isFilterable={false}
                      />
                <Layout
                  header={<SearchBox autocompleteSuggestions={true} />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Sort"}
                          sortOptions={buildSortOptionsFromConfig()}
                          view={SortingView}
                        />
                      )}
                      <Facet
                        field="city"
                        label="City"
                        filterType="any"
                        view={MultiCheckboxFacet}
                        isFilterable={true}
                      />
                      <Facet
                        field="diversity_focus"
                        label="Diversity Focus"
                        filterType="any"
                        view={MultiCheckboxFacet}
                      />
                      <Facet
                        field="technology_focus"
                        label="Technology Focus"
                        filterType="any"
                        view={MultiCheckboxFacet}
                        isFilterable={true}
                      />
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={getConfig().titleField}
                      urlField={getConfig().urlField}
                      shouldTrackClickThrough={true}
                      resultView={Result}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
    <footer>
        <p>
            Made by <a href="https://kjaymiller.com">kjaymiller</a>
        </p>
        <p><a href="./about.html"><strong>About</strong></a></p>
    </footer>
      </div>
  );
}

