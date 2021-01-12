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
    const flexStyle = {
        "display": "flex",
        "flexFlow": "space-around",
        "alignItems": "center",
        "border": "1px solid #777",
        "borderRadius": "5px",
        "padding": "50px",
        "margin": "5px",
        "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    }
    const imgStyle = {
        "maxWidth": "75px",
        "maxHeight": "75px",
        "marginRight": "25px",
        "marginLeft": "15px"
    }

    const smallStyle = {
        "borderRadius": "5px",
        "padding": "5px",
        "border": "1px solid #777",
        "margin": "10px 5px 5px 5px"
    }
    const parentOrg = props.result.parent_organization.snippet

    function smallDivs (field) {
        return field ? <small style={smallStyle}>{field}</small> : ''
    }

    return (
        <div style={flexStyle}>
            <img 
                src={props.result.organization_logo.raw}
                alt={parentOrg} Logo
                style={imgStyle}
            />
            <div>
                {smallDivs(parentOrg)}
                {smallDivs(props.result.city.raw)}
                <h1>{props.result.url.raw ? hasLink : noLink}</h1>
        {props.result.diversity_focus.raw.map((o) => smallDivs(o))}
            </div>
        </div>
    )
} 

export default function App() {
  return (
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
                        field="diversity_focus"
                        label="Diversity Focus"
                        filterType="any"
                        view={MultiCheckboxFacet}
                        isFilterable={true}
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
  );
}
