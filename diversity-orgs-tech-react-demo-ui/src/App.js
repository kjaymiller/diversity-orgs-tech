import React from "react";

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
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildAutocompleteQueryConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
} from "./config/config-helper";

import SortingView from './SortingView';
import MultiCheckboxFacet from './FacetView';

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
  alwaysSearchOnInitialLoad: true
};


function ResultView(props) {
    
    const hasLink = <a href={props.result.url.snippet}>
          {props.result.name.raw}
        </a>

    const noLink = props.result.name.raw

    function parentOrg () { 
        if (props.result.parent_organization.snippet) {
            return <small className="parentOrg mx-2">{props.result.parent_organization.snippet}</small>
        }
        return ''
    }

    function smallDivs (field) {
        return field ? <small className="mx-2">{field}</small> : ''
    }

    return (
        <div className="lg:flex lg:jusitify-between items-center rounded-lg shadow-lg p-6">
            <div className="lg:w-3/4 w-1/4 lg:p-8">
                <img 
                    src={props.result.organization_logo.raw}
                    alt={parentOrg} Logo
                />
            </div>
            <div className="">
                {props.result.diversity_focus.raw.map((o) => smallDivs(o))}
                {parentOrg()}
                <h1 className="text-3xl my-3">{props.result.url.raw ? hasLink : noLink}</h1>
                {smallDivs(props.result.city.raw)}
            </div>
        </div>
    )
} 

export default function App() {
  return (
    <div className="container px-2 mx-auto my-4">
        <div>
        <h1><a href="/">DiversityOrgs.Tech</a></h1>
        <h2 className="my-4 text-3xl">Find the tech community that's right for you.</h2>
        <p>This is a tool to help folks from underrepresented groups. Search for groups based on their Representation goals or their tech stack.</p>
        <p>If you can't find a group in your area or you know of one we're missing, then let us know with the contact form below.</p>
    </div>
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
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
                        field="parent_organization"
                        label="Parent Organization"
                        view={MultiCheckboxFacet}
                        isFilterable={false}
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
                      resultView={ResultView}
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
